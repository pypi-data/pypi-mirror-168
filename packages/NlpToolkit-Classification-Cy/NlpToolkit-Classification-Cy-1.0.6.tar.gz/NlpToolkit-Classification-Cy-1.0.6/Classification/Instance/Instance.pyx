from Classification.Attribute.DiscreteAttribute cimport DiscreteAttribute
from Classification.Attribute.ContinuousAttribute cimport ContinuousAttribute


cdef class Instance(object):

    def __init__(self,
                 classLabel: str,
                 attributes=None):
        """
        Constructor for a single instance. Given the attributes and class label, it generates a new instance.

        PARAMETERS
        ----------
        classLabel : str
            Class label of the instance.
        attributes : list
            Attributes of the instance.
        """
        if attributes is None:
            attributes = []
        self.__class_label = classLabel
        self.__attributes = attributes

    def __lt__(self, other):
        return self.__class_label < other.classLabel

    def __gt__(self, other):
        return self.__class_label > other.classLabel

    def __eq__(self, other):
        return self.__class_label == other.classLabel

    cpdef addDiscreteAttribute(self, str value):
        """
        Adds a discrete attribute with the given String value.

        PARAMETERS
        ----------
        value : str
            Value of the discrete attribute.
        """
        self.__attributes.append(DiscreteAttribute(value))

    cpdef addContinuousAttribute(self, double value):
        """
        Adds a continuous attribute with the given float value.

        PARAMETERS
        ----------
        value : float
            Value of the continuous attribute.
        """
        self.__attributes.append(ContinuousAttribute(value))

    cpdef addAttribute(self, Attribute attribute):
        """
        Adds a new attribute.

        PARAMETERS
        ----------
        attribute : Attribute
            Attribute to be added.
        """
        self.__attributes.append(attribute)

    cpdef addVectorAttribute(self, Vector vector):
        """
        Adds a Vector of continuous attributes.

        PARAMETERS
        ----------
        vector : Vector
            Vector that has the continuous attributes.
        """
        cdef int i
        for i in range(vector.size()):
            self.__attributes.append(ContinuousAttribute(vector.getValue(i)))

    cpdef removeAttribute(self, int index):
        """
        Removes attribute with the given index from the attributes list.

        PARAMETERS
        ----------
        index : int
            Index of the attribute to be removed.
        """
        self.__attributes.pop(index)

    cpdef removeAllAttributes(self):
        """
        Removes all the attributes from the attributes list.
        """
        self.__attributes.clear()

    cpdef Attribute getAttribute(self, int index):
        """
        Accessor for a single attribute.

        PARAMETERS
        ----------
        index : int
            Index of the attribute to be accessed.

        RETURNS
        -------
        Attribute
            Attribute with index 'index'.
        """
        return self.__attributes[index]

    cpdef int attributeSize(self):
        """
        Returns the number of attributes in the attributes list.

        RETURNS
        -------
        int
            Number of attributes in the attributes list.
        """
        return len(self.__attributes)

    cpdef int continuousAttributeSize(self):
        """
        Returns the number of continuous and discrete indexed attributes in the attributes list.

        RETURNS
        -------
        int
            Number of continuous and discrete indexed attributes in the attributes list.
        """
        cdef int size
        cdef Attribute attribute
        size = 0
        for attribute in self.__attributes:
            size += attribute.continuousAttributeSize()
        return size

    cpdef list continuousAttributes(self):
        """
        The continuousAttributes method creates a new list result and it adds the continuous attributes of the
        attributes list and also it adds 1 for the discrete indexed attributes.

        RETURNS
        -------
        list
            result list that has continuous and discrete indexed attributes.
        """
        cdef list result
        cdef Attribute attribute
        result = []
        for attribute in self.__attributes:
            result.extend(attribute.continuousAttributes())
        return result

    cpdef str getClassLabel(self):
        """
        Accessor for the class label.

        RETURNS
        -------
        str
            Class label of the instance.
        """
        return self.__class_label

    def __str__(self) -> str:
        """
        Converts instance to a String.

        RETURNS
        -------
        str
            A string of attributes separated with comma character.
        """
        cdef str result
        cdef Attribute attribute
        result = ""
        for attribute in self.__attributes:
            result = result + attribute.__str__() + ","
        result = result + self.__class_label
        return result

    cpdef Instance getSubSetOfFeatures(self, FeatureSubSet featureSubSet):
        """
        The getSubSetOfFeatures method takes a FeatureSubSet as an input. First it creates a result Instance
        with the class label, and adds the attributes of the given featureSubSet to it.

        PARAMETERS
        ----------
        featureSubSet : FeatureSubSet
            FeatureSubSet an list of indices.

        RETURNS
        -------
        Instance
            result Instance.
        """
        cdef Instance result
        cdef int i
        result = Instance(self.__class_label)
        for i in range(featureSubSet.size()):
            result.addAttribute(self.__attributes[featureSubSet.get(i)])
        return result

    cpdef Vector toVector(self):
        """
        The toVector method returns a Vector of continuous attributes and discrete indexed attributes.

        RETURNS
        -------
        Vector
            Vector of continuous attributes and discrete indexed attributes.
        """
        cdef list result
        cdef Attribute attribute
        values = []
        for attribute in self.__attributes:
            values.extend(attribute.continuousAttributes())
        return Vector(values)
