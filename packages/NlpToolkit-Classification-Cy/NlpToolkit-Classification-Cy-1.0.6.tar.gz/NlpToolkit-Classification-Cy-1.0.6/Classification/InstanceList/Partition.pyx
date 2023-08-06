import random
from Classification.InstanceList.InstanceListOfSameClass cimport InstanceListOfSameClass
from Math.DiscreteDistribution cimport DiscreteDistribution
from Classification.Instance.Instance cimport Instance


cdef class Partition(object):

    def __init__(self,
                 instanceList: InstanceList = None,
                 ratio=None, seed=None,
                 stratified: bool = None):
        """
        Divides the instances in the instance list into partitions so that all instances of a class are grouped in a
        single partition.
        PARAMETERS
        ----------
        ratio
            Ratio of the stratified partition. Ratio is between 0 and 1. If the ratio is 0.2, then 20 percent of the
            instances are put in the first group, 80 percent of the instances are put in the second group.
        seed
            seed is used as a random number.
        """
        cdef list class_labels, counts, random_array, value_list
        cdef str class_label
        cdef Instance instance
        cdef DiscreteDistribution distribution
        cdef int i, class_index, attribute_index, attribute_value
        cdef double split_value
        self.__multi_list = []
        if instanceList is not None:
            if ratio is None:
                class_labels = instanceList.getDistinctClassLabels()
                for class_label in class_labels:
                    self.add(InstanceListOfSameClass(class_label))
                for instance in instanceList.getInstances():
                    self.get(class_labels.index(instance.getClassLabel())).add(instance)
            else:
                if isinstance(ratio, float):
                    self.add(InstanceList())
                    self.add(InstanceList())
                    if stratified:
                        distribution = instanceList.classDistribution()
                        counts = [0] * len(distribution)
                        random_array = [i for i in range(instanceList.size())]
                        random.seed(seed)
                        random.shuffle(random_array)
                        for i in range(instanceList.size()):
                            instance = instanceList.get(random_array[i])
                            class_index = distribution.getIndex(instance.getClassLabel())
                            if counts[class_index] < instanceList.size() * ratio * \
                                    distribution.getProbability(instance.getClassLabel()):
                                self.get(0).add(instance)
                            else:
                                self.get(1).add(instance)
                            counts[class_index] = counts[class_index] + 1
                    else:
                        instanceList.shuffle(seed)
                        for i in range(self.size()):
                            instance = instanceList.get(i)
                            if i < instanceList.size() * ratio:
                                self.get(0).add(instance)
                            else:
                                self.get(1).add(instance)
                elif isinstance(ratio, int):
                    attribute_index = ratio
                    if seed is None:
                        value_list = instanceList.getAttributeValueList(attribute_index)
                        for _ in value_list:
                            self.add(InstanceList())
                        for instance in instanceList.getInstances():
                            self.get(value_list.index(instance.getAttribute(attribute_index).getValue())).add(instance)
                    elif isinstance(seed, int):
                        attribute_value = seed
                        self.add(InstanceList())
                        self.add(InstanceList())
                        for instance in instanceList.getInstances():
                            if instance.getAttribute(attribute_index).getIndex() == attribute_value:
                                self.get(0).add(instance)
                            else:
                                self.get(1).add(instance)
                    elif isinstance(seed, float):
                        split_value = seed
                        self.add(InstanceList())
                        self.add(InstanceList())
                        for instance in instanceList.getInstances():
                            if instance.getAttribute(attribute_index).getValue() < split_value:
                                self.get(0).add(instance)
                            else:
                                self.get(1).add(instance)

    cpdef add(self, InstanceList _list):
        """
        Adds given instance list to the list of instance lists.

        PARAMETERS
        ----------
        _list : InstanceList
            Instance list to add.
        """
        self.__multi_list.append(_list)

    cpdef int size(self):
        """
        Returns the size of the list of instance lists.

        RETURNS
        -------
        int
            The size of the list of instance lists.
        """
        return len(self.__multi_list)

    cpdef InstanceList get(self, int index):
        """
        Returns the corresponding instance list at given index of list of instance lists.

        PARAMETERS
        ----------
        index : int
            Index of the instance list.

        RETURNS
        -------
        InstanceList
            Instance list at given index of list of instance lists.
        """
        return self.__multi_list[index]

    cpdef list getLists(self):
        """
        Returns the instances of the items at the list of instance lists.

        RETURNS
        -------
        list
            Instances of the items at the list of instance lists.
        """
        cdef list result
        cdef InstanceList instance_list
        result = []
        for instance_list in self.__multi_list:
            result.append(instance_list.getInstances())
        return result
