from Classification.Attribute.AttributeType import AttributeType
from Classification.Instance.CompositeInstance cimport CompositeInstance
from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.BinaryAttribute cimport BinaryAttribute
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.InstanceList.Partition cimport Partition


cdef class DataSet(object):

    def __init__(self,
                 definition: DataDefinition = None,
                 separator: str = None,
                 fileName: str = None):
        """
        Constructor for generating a new DataSet with given DataDefinition.

        PARAMETERS
        ----------
        definition : DataDefinition
            Data definition of the data set.
        separator : str
            Separator character which separates the attribute values in the data file.
        fileName : str
            Name of the data set file.
        """
        self.__definition = definition
        if separator is None:
            self.__instances = InstanceList()
        else:
            self.__instances = InstanceList(listOrDefinition=definition,
                                            separator=separator,
                                            fileName=fileName)

    cpdef initWithFile(self, str fileName):
        """
        Constructor for generating a new DataSet from given File.

        PARAMETERS
        ----------
        fileName : str
            File to generate DataSet from.
        """
        cdef int i
        cdef list lines, attributes, labels
        cdef str line
        cdef Instance instance
        self.__instances = InstanceList()
        self.__definition = DataDefinition()
        input_file = open(fileName, 'r', encoding='utf8')
        lines = input_file.readlines()
        input_file.close()
        i = 0
        for line in lines:
            attributes = line.split(",")
            if i == 0:
                for j in range(len(attributes) - 1):
                    try:
                        float(attributes[j])
                        self.__definition.addAttribute(AttributeType.CONTINUOUS)
                    except:
                        self.__definition.addAttribute(AttributeType.DISCRETE)
            else:
                if len(attributes) != self.__definition.attributeCount() + 1:
                    continue
            if ";" not in attributes[len(attributes) - 1]:
                instance = Instance(attributes[len(attributes) - 1])
            else:
                labels = attributes[len(attributes) - 1].split(";")
                instance = CompositeInstance(labels[0], None, labels)
            for j in range(len(attributes) - 1):
                if self.__definition.getAttributeType(j) is AttributeType.CONTINUOUS:
                    instance.addAttribute(ContinuousAttribute(float(attributes[j])))
                elif self.__definition.getAttributeType(j) is AttributeType.DISCRETE:
                    instance.addAttribute(DiscreteAttribute(attributes[j]))
            if instance.attributeSize() == self.__definition.attributeCount():
                self.__instances.add(instance)
            i = i + 1

    cpdef bint __checkDefinition(self, Instance instance):
        """
        Checks the correctness of the attribute type, for instance, if the attribute of given instance is a Binary
        attribute, and the attribute type of the corresponding item of the data definition is also a Binary attribute,
        it then returns true, and false otherwise.

        PARAMETERS
        ----------
        instance : Instance
            Instance to checks the attribute type.

        RETURNS
        -------
        bool
            true if attribute types of given Instance and data definition matches.
        """
        cdef int i
        for i in range(instance.attributeSize()):
            if isinstance(instance.getAttribute(i), BinaryAttribute):
                if self.__definition.getAttributeType(i) is not AttributeType.BINARY:
                    return False
            elif isinstance(instance.getAttribute(i), DiscreteIndexedAttribute):
                if self.__definition.getAttributeType(i) is not AttributeType.DISCRETE_INDEXED:
                    return False
            elif isinstance(instance.getAttribute(i), DiscreteAttribute):
                if self.__definition.getAttributeType(i) is not AttributeType.DISCRETE:
                    return False
            elif isinstance(instance.getAttribute(i), ContinuousAttribute):
                if self.__definition.getAttributeType(i) is not AttributeType.CONTINUOUS:
                    return False
        return True

    cpdef __setDefinition(self, Instance instance):
        """
        Adds the attribute types according to given Instance. For instance, if the attribute type of given Instance
        is a Discrete type, it than adds a discrete attribute type to the list of attribute types.

        PARAMETERS
        ----------
        instance : Instance
            Instance input.
        """
        cdef list attribute_types
        cdef int i
        attribute_types = []
        for i in range(instance.attributeSize()):
            if isinstance(instance.getAttribute(i), BinaryAttribute):
                attribute_types.append(AttributeType.BINARY)
            elif isinstance(instance.getAttribute(i), DiscreteIndexedAttribute):
                attribute_types.append(AttributeType.DISCRETE_INDEXED)
            elif isinstance(instance.getAttribute(i), DiscreteAttribute):
                attribute_types.append(AttributeType.DISCRETE)
            elif isinstance(instance.getAttribute(i), ContinuousAttribute):
                attribute_types.append(AttributeType.CONTINUOUS)
        self.__definition = DataDefinition(attribute_types)

    cpdef int sampleSize(self):
        """
        Returns the size of the InstanceList.

        RETURNS
        -------
        int
            Size of the InstanceList.
        """
        return self.__instances.size()

    cpdef int classCount(self):
        """
        Returns the size of the class label distribution of InstanceList.

        RETURNS
        -------
        int
            Size of the class label distribution of InstanceList.
        """
        return len(self.__instances.classDistribution())

    cpdef int attributeCount(self):
        """
        Returns the number of attribute types at DataDefinition list.

        RETURNS
        -------
        int
            The number of attribute types at DataDefinition list.
        """
        return self.__definition.attributeCount()

    cpdef int discreteAttributeCount(self):
        """
        Returns the number of discrete attribute types at DataDefinition list.

        RETURNS
        -------
        int
            The number of discrete attribute types at DataDefinition list.
        """
        return self.__definition.discreteAttributeCount()

    cpdef int continuousAttributeCount(self):
        """
        Returns the number of continuous attribute types at DataDefinition list.

        RETURNS
        -------
        int
            The number of continuous attribute types at DataDefinition list.
        """
        return self.__definition.continuousAttributeCount()

    cpdef str getClasses(self):
        """
        Returns the accumulated String of class labels of the InstanceList.

        RETURNS
        -------
        str
            The accumulated String of class labels of the InstanceList.
        """
        cdef list class_labels
        cdef str result
        cdef int i
        class_labels = self.__instances.getDistinctClassLabels()
        result = class_labels[0]
        for i in range(1, len(class_labels)):
            result = result + ";" + class_labels[i]
        return result

    cpdef str info(self, str dataSetName):
        """
        Returns the general information about the given data set such as the number of instances, distinct class labels,
        attributes, discrete and continuous attributes.

        PARAMETERS
        ----------
        dataSetName : str
            Data set name.

        RETURNS
        -------
        str
            General information about the given data set.
        """
        cdef str result
        result = "DATASET: " + dataSetName + "\n"
        result = result + "Number of instances: " + self.sampleSize().__str__() + "\n"
        result = result + "Number of distinct class labels: " + self.classCount().__str__() + "\n"
        result = result + "Number of attributes: " + self.attributeCount().__str__() + "\n"
        result = result + "Number of discrete attributes: " + self.discreteAttributeCount().__str__() + "\n"
        result = result + "Number of continuous attributes: " + self.continuousAttributeCount().__str__() + "\n"
        result = result + "Class labels: " + self.getClasses()
        return result

    cpdef addInstance(self, Instance current):
        """
        Adds a new instance to the InstanceList.

        PARAMETERS
        ----------
        current : Instance
            Instance to add.
        """
        if self.__definition is None:
            self.__setDefinition(current)
            self.__instances.add(current)
        elif self.__checkDefinition(current):
            self.__instances.add(current)

    cpdef addInstanceList(self, list instanceList):
        """
        Adds all the instances of given instance list to the InstanceList.

        PARAMETERS
        ----------
        instanceList : list
            InstanceList to add instances from.
        """

        for instance in instanceList:
            self.addInstance(instance)

    cpdef list getInstances(self):
        """
        Returns the instances of InstanceList.

        RETURNS
        -------
        list
            The instances of InstanceList.
        """
        return self.__instances.getInstances()

    cpdef list getClassInstances(self):
        """
        Returns instances of the items at the list of instance lists from the partitions.

        RETURNS
        -------
        list
            Instances of the items at the list of instance lists from the partitions.
        """
        return Partition(self.__instances).getLists()

    cpdef InstanceList getInstanceList(self):
        """
        Accessor for the InstanceList.

        RETURNS
        -------
        InstanceList
            The InstanceList.
        """
        return self.__instances

    cpdef DataDefinition getDataDefinition(self):
        """
        Accessor for the data definition.

        RETURNS
        -------
        DataDefinition
            The data definition.
        """
        return self.__definition

    cpdef DataSet getSubSetOfFeatures(self, FeatureSubSet featureSubSet):
        """
        Return a subset generated via the given FeatureSubSet.

        PARAMETERS
        ----------
        featureSubSet : FeatureSubSet
            FeatureSubSet input.

        RETURNS
        -------
        FeatureSubSet
            Subset generated via the given FeatureSubSet.
        """
        cdef DataSet result
        cdef int i
        result = DataSet(self.__definition.getSubSetOfFeatures(featureSubSet))
        for i in range(self.__instances.size()):
            result.addInstance(self.__instances.get(i).getSubSetOfFeatures(featureSubSet))
        return result

    cpdef writeToFile(self, str outFileName):
        """
        Print out the instances of InstanceList as a String.

        PARAMETERS
        ----------
        outFileName : str
            File name to write the output.
        """
        cdef int i
        out_file = open(outFileName, "w")
        for i in range(self.__instances.size()):
            out_file.write(self.__instances.get(i).__str__() + "\n")
        out_file.close()
