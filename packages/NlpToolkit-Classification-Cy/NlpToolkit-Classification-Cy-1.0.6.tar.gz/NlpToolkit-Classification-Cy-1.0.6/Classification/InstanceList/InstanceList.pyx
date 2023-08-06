import random
import math
from functools import cmp_to_key

from Classification.DataSet.DataDefinition cimport DataDefinition
from Classification.Attribute.AttributeType import AttributeType
from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.BinaryAttribute cimport BinaryAttribute
from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute
from Classification.Instance.CompositeInstance cimport CompositeInstance
from Classification.Attribute.DiscreteIndexedAttribute cimport DiscreteIndexedAttribute
from Classification.Model.Model cimport Model


cdef class InstanceList(object):

    def __init__(self,
                 listOrDefinition = None,
                 separator: str = None,
                 fileName: str = None):
        """
        Constructor for an instance list with a given data definition, data file and a separator character. Each
        instance must be stored in a separate line separated with the character separator. The last item must be the
        class label. The function reads the file line by line and for each line; depending on the data definition, that
        is, type of the attributes, adds discrete and continuous attributes to a new instance. For example, given the
        data set file

        red;1;0.4;true
        green;-1;0.8;true
        blue;3;1.3;false

        where the first attribute is a discrete attribute, second and third attributes are continuous attributes, the
        fourth item is the class label.

        PARAMETERS
        ----------
        listOrDefinition
            Data definition of the data set.
        separator : str
            Separator character which separates the attribute values in the data file.
        fileName : str
            Name of the data set file.
        """
        cdef list lines, attribute_list
        cdef str line
        cdef Instance current
        cdef int i
        if listOrDefinition is None:
            self.list = []
        else:
            if separator is None and isinstance(listOrDefinition, list):
                self.list = listOrDefinition
            else:
                if isinstance(listOrDefinition, DataDefinition):
                    self.list = []
                    file = open(fileName, 'r', encoding='utf8')
                    lines = file.readlines()
                    file.close()
                    for line in lines:
                        attribute_list = line.strip().split(separator)
                        if len(attribute_list) == listOrDefinition.attributeCount() + 1:
                            current = Instance(attribute_list[len(attribute_list) - 1])
                            for i in range(len(attribute_list) - 1):
                                if listOrDefinition.getAttributeType(i) is AttributeType.DISCRETE:
                                    current.addAttribute(DiscreteAttribute(attribute_list[i]))
                                elif listOrDefinition.getAttributeType(i) is AttributeType.BINARY:
                                    current.addAttribute(
                                        BinaryAttribute(attribute_list[i] in ["True", "true", "Yes", "yes", "y", "Y"]))
                                elif listOrDefinition.getAttributeType(i) is AttributeType.CONTINUOUS:
                                    current.addAttribute(ContinuousAttribute(float(attribute_list[i])))
                            self.list.append(current)

    cpdef add(self, Instance instance):
        """
        Adds instance to the instance list.

        PARAMETERS
        ----------
        instance : Instance
            Instance to be added.
        """
        self.list.append(instance)

    cpdef addAll(self, list instanceList):
        """
        Adds a list of instances to the current instance list.

        PARAMETERS
        ----------
        instanceList : list
            List of instances to be added.
        """
        self.list.extend(instanceList)

    cpdef int size(self):
        """
        Returns size of the instance list.

        RETURNS
        -------
        int
            Size of the instance list.
        """
        return len(self.list)

    cpdef Instance get(self, int index):
        """
        Accessor for a single instance with the given index.

        PARAMETERS
        ----------
        index : int
            Index of the instance.

        RETURNS
        -------
        Instance
            Instance with index 'index'.
        """
        return self.list[index]

    def makeComparator(self, attributeIndex: int):
        def compare(instanceA: Instance, instanceB: Instance):
            result1 = instanceA.getAttribute(attributeIndex).getValue()
            result2 = instanceB.getAttribute(attributeIndex).getValue()
            if result1 < result2:
                return -1
            elif result1 > result2:
                return 1
            else:
                return 0
        return compare

    cpdef sortWrtAttribute(self, int attributeIndex):
        """
        Sorts attribute list according to the attribute with index 'attributeIndex'.

        PARAMETERS
        ----------
        attributeIndex : int
            index of the attribute.
        """
        self.list.sort(key=cmp_to_key(self.makeComparator(attributeIndex)))

    cpdef sort(self):
        """
        Sorts attributes list.
        """
        self.list.sort()

    cpdef shuffle(self, int seed):
        """
        Shuffles the instance list.

        PARAMETERS
        ----------
        seed : int
            Seed is used for random number generation.
        """
        random.seed(seed)
        random.shuffle(self.list)

    cpdef Bootstrap bootstrap(self, int seed):
        """
        Creates a bootstrap sample from the current instance list.

        PARAMETERS
        ----------
        seed : int
            To create a different bootstrap sample, we need a new seed for each sample.

        RETURNS
        -------
        Bootstrap
            Bootstrap sample.
        """
        return Bootstrap(self.list, seed)

    cpdef list getClassLabels(self):
        """
        Extracts the class labels of each instance in the instance list and returns them in an array of {@link String}.

        RETURNS
        -------
        list
            A list of class labels.
        """
        cdef list class_labels
        cdef Instance instance
        class_labels = []
        for instance in self.list:
            class_labels.append(instance.getClassLabel())
        return class_labels

    cpdef list getDistinctClassLabels(self):
        """
        Extracts the class labels of each instance in the instance list and returns them as a set.

        RETURNS
        -------
        list
            A list of distinct class labels.
        """
        cdef list class_labels
        cdef Instance instance
        class_labels = []
        for instance in self.list:
            if not instance.getClassLabel() in class_labels:
                class_labels.append(instance.getClassLabel())
        return class_labels

    cpdef list getUnionOfPossibleClassLabels(self):
        """
        Extracts the possible class labels of each instance in the instance list and returns them as a set.

        RETURNS
        -------
        list
            A list of distinct class labels.
        """
        cdef list possible_class_labels
        cdef Instance instance
        cdef str possible_class_label
        possible_class_labels = []
        for instance in self.list:
            if isinstance(instance, CompositeInstance):
                for possible_class_label in instance.getPossibleClassLabels():
                    if possible_class_label not in possible_class_labels:
                        possible_class_labels.append(possible_class_label)
            else:
                if not instance.getClassLabel() in possible_class_labels:
                    possible_class_labels.append(instance.getClassLabel())
        return possible_class_labels

    cpdef list getAttributeValueList(self, int attributeIndex):
        """
        Extracts distinct discrete values of a given attribute as an array of strings.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the discrete attribute.

        RETURNS
        -------
        list
            An list of distinct values of a discrete attribute.
        """
        cdef list value_list
        cdef Instance instance
        value_list = []
        for instance in self.list:
            if not instance.getAttribute(attributeIndex).getValue() in value_list:
                value_list.append(instance.getAttribute(attributeIndex).getValue())
        return value_list

    cpdef Attribute __attributeAverage(self, int index):
        """
        Calculates the mean of a single attribute for this instance list (m_i). If the attribute is discrete, the
        maximum occurring value for that attribute is returned. If the attribute is continuous, the mean value of the
        values of all instances are returned.

        PARAMETERS
        ----------
        index : int
            Index of the attribute.

        RETURNS
        -------
        Attribute
            The mean value of the instances as an attribute.
        """
        cdef list values
        cdef Instance instance
        cdef double total
        if isinstance(self.list[0].getAttribute(index), DiscreteAttribute):
            values = []
            for instance in self.list:
                values.append(instance.getAttribute(index).getValue())
            return DiscreteAttribute(Model.getMaximum(values))
        elif isinstance(self.list[0].getAttribute(index), ContinuousAttribute):
            total = 0.0
            for instance in self.list:
                total += instance.getAttribute(index).getValue()
            return ContinuousAttribute(total / len(self.list))
        else:
            return None

    cpdef list continuousAttributeAverage(self, int index):
        """
        Calculates the mean of a single attribute for this instance list (m_i).

        PARAMETERS
        ----------
        index : int
            Index of the attribute.

        RETURNS
        -------
        list
            The mean value of the instances as an attribute.
        """
        cdef int max_index_size, i, value_index
        cdef list values
        cdef Instance instance
        cdef double total
        if isinstance(self.list[0].getAttribute(index), DiscreteIndexedAttribute):
            max_index_size = self.list[0].getAttribute(index).getMaxIndex()
            values = [0.0] * max_index_size
            for instance in self.list:
                value_index = instance.getAttribute(index).getIndex()
                values[value_index] = values[value_index] + 1
            for i in range(len(values)):
                values[i] = values[i] / len(self.list)
            return values
        elif isinstance(self.list[0].getAttribute(index), ContinuousAttribute):
            total = 0.0
            for instance in self.list:
                total += instance.getAttribute(index).getValue()
            return [total / len(self.list)]
        else:
            return None

    cpdef Attribute __attributeStandardDeviation(self, int index):
        """
        Calculates the standard deviation of a single attribute for this instance list (m_i). If the attribute is
        discrete, None returned. If the attribute is continuous, the standard deviation  of the values all instances are
        returned.

        PARAMETERS
        ----------
        index : int
            Index of the attribute.

        RETURNS
        -------
        Attribute
            The standard deviation of the instances as an attribute.
        """
        cdef double total, average
        cdef Instance instance
        if isinstance(self.list[0].getAttribute(index), ContinuousAttribute):
            total = 0.0
            for instance in self.list:
                total += instance.getAttribute(index).getValue()
            average = total / len(self.list)
            total = 0.0
            for instance in self.list:
                total += math.pow(instance.getAttribute(index).getValue() - average, 2)
            return ContinuousAttribute(math.sqrt(total / (len(self.list) - 1)))
        else:
            return None

    cpdef list continuousAttributeStandardDeviation(self, int index):
        """
        Calculates the standard deviation of a single continuous attribute for this instance list (m_i).

        PARAMETERS
        ----------
        index : int
            Index of the attribute.

        RETURNS
        -------
        list
            The standard deviation of the instances as an attribute.
        """
        cdef int max_index_size, value_index, i
        cdef list averages, values
        cdef Instance instance
        cdef double total, average
        if isinstance(self.list[0].getAttribute(index), DiscreteIndexedAttribute):
            max_index_size = self.list[0].getAttribute(index).getMaxIndex()
            averages = [0.0] * max_index_size
            for instance in self.list:
                value_index = instance.getAttribute(index).getIndex()
                averages[value_index] = averages[value_index] + 1
            for i in range(len(averages)):
                averages[i] = averages[i] / len(self.list)
            values = [0.0] * max_index_size
            for instance in self.list:
                value_index = instance.getAttribute(index).getIndex()
                for i in range(max_index_size):
                    if i == value_index:
                        values[i] += math.pow(1 - averages[i], 2)
                    else:
                        values[i] += math.pow(averages[i], 2)
            for i in range(len(values)):
                values[i] = math.sqrt(values[i] / (len(self.list) - 1))
            return values
        elif isinstance(self.list[0].getAttribute(index), ContinuousAttribute):
            total = 0.0
            for instance in self.list:
                total += instance.getAttribute(index).getValue()
            average = total / len(self.list)
            for instance in self.list:
                total += math.pow(instance.getAttribute(index).getValue() - average, 2)
            return [math.sqrt(total / (len(self.list) - 1))]
        else:
            return None

    cpdef DiscreteDistribution attributeDistribution(self, int index):
        """
        The attributeDistribution method takes an index as an input and if the attribute of the instance at given index
        is discrete, it returns the distribution of the attributes of that instance.

        PARAMETERS
        ----------
        index : int
            Index of the attribute.

        RETURNS
        -------
        DiscreteDistribution
            Distribution of the attribute.
        """
        cdef DiscreteDistribution distribution
        cdef Instance instance
        distribution = DiscreteDistribution()
        if isinstance(self.list[0].getAttribute(index), DiscreteAttribute):
            for instance in self.list:
                distribution.addItem(instance.getAttribute(index).getValue())
        return distribution

    cpdef list attributeClassDistribution(self, int attributeIndex):
        """
        The attributeClassDistribution method takes an attribute index as an input. It loops through the instances, gets
        the corresponding value of given attribute index and adds the class label of that instance to the discrete
        distributions list.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.

        RETURNS
        -------
        list
            Distribution of the class labels.
        """
        cdef list distributions, value_list
        cdef Instance instance
        distributions = []
        value_list = self.getAttributeValueList(attributeIndex)
        for _ in value_list:
            distributions.append(DiscreteDistribution())
        for instance in self.list:
            distributions[value_list.index(instance.getAttribute(attributeIndex).getValue())].addItem(instance.
                                                                                                     getClassLabel())
        return distributions

    cpdef DiscreteDistribution discreteIndexedAttributeClassDistribution(self, int attributeIndex, int attributeValue):
        """
        The discreteIndexedAttributeClassDistribution method takes an attribute index and an attribute value as inputs.
        It loops through the instances, gets the corresponding value of given attribute index and given attribute value.
        Then, adds the class label of that instance to the discrete indexed distributions list.

        PARAMETERS
        ----------
        attributeIndex : int
            Index of the attribute.
        attributeValue : int
            Value of the attribute.

        RETURNS
        -------
        DiscreteDistribution
            Distribution of the class labels.
        """
        cdef DiscreteDistribution distribution
        cdef Instance instance
        distribution = DiscreteDistribution()
        for instance in self.list:
            if instance.getAttribute(attributeIndex).getIndex() == attributeValue:
                distribution.addItem(instance.getClassLabel())
        return distribution

    cpdef DiscreteDistribution classDistribution(self):
        """
        The classDistribution method returns the distribution of all the class labels of instances.

        RETURNS
        -------
        DiscreteDistribution
            Distribution of the class labels.
        """
        cdef DiscreteDistribution distribution
        cdef Instance instance
        distribution = DiscreteDistribution()
        for instance in self.list:
            distribution.addItem(instance.getClassLabel())
        return distribution

    cpdef list allAttributesDistribution(self):
        """
        The allAttributesDistribution method returns the distributions of all the attributes of instances.

        RETURNS
        -------
        list
            Distributions of all the attributes of instances.
        """
        cdef list distributions
        cdef int i
        distributions = []
        for i in range(self.list[0].attributeSize()):
            distributions.append(self.attributeDistribution(i))
        return distributions

    cpdef Instance average(self):
        """
        Returns the mean of all the attributes for instances in the list.

        RETURNS
        -------
        Instance
            Mean of all the attributes for instances in the list.
        """
        cdef Instance result
        cdef int i
        result = Instance(self.list[0].getClassLabel())
        for i in range(self.list[0].attributeSize()):
            result.addAttribute(self.__attributeAverage(i))
        return result

    cpdef list continuousAverage(self):
        """
        Calculates mean of the attributes of instances.

        RETURNS
        -------
        list
            Mean of the attributes of instances.
        """
        cdef list result
        cdef int i
        result = []
        for i in range(self.list[0].attributeSize()):
            result.extend(self.continuousAttributeAverage(i))
        return result

    cpdef Instance standardDeviation(self):
        """
        Returns the standard deviation of attributes for instances.

        RETURNS
        -------
        Instance
            Standard deviation of attributes for instances.
        """
        cdef Instance result
        cdef int i
        result = Instance(self.list[0].getClassLabel())
        for i in range(self.list[0].attributeSize()):
            result.addAttribute(self.__attributeStandardDeviation(i))
        return result

    cpdef list continuousStandardDeviation(self):
        """
        Returns the standard deviation of continuous attributes for instances.

        RETURNS
        -------
        list
            Standard deviation of continuous attributes for instances.
        """
        cdef list result
        cdef int i
        result = []
        for i in range(self.list[0].attributeSize()):
            result.extend(self.continuousAttributeStandardDeviation(i))
        return result

    cpdef Matrix covariance(self, Vector average):
        """
        Calculates a covariance Matrix by using an average Vector.

        PARAMETERS
        ----------
        average : Vector
            Vector input.

        RETURNS
        -------
        Matrix
            Covariance Matrix.
        """
        cdef Matrix result
        cdef Instance instance
        cdef list continuous_attributes
        cdef int i
        cdef double xi, mi, xj, mj
        result = Matrix(self.list[0].continuousAttributeSize(), self.list[0].continuousAttributeSize())
        for instance in self.list:
            continuous_attributes = instance.continuousAttributes()
            for i in range(instance.continuousAttributeSize()):
                xi = continuous_attributes[i]
                mi = average.getValue(i)
                for j in range(instance.continuousAttributeSize()):
                    xj = continuous_attributes[j]
                    mj = average.getValue(j)
                    result.addValue(i, j, (xi - mi) * (xj - mj))
        result.divideByConstant(len(self.list) - 1)
        return result

    cpdef list getInstances(self):
        """
        Accessor for the instances.

        RETURNS
        -------
        list
            Instances.
        """
        return self.list
