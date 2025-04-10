class BSTHeap:

    def __init__(self, size):
        self.HeapTree = [None] * size
        self.num_elements = 0

    def insert(self, key):
        self.HeapTree[self.num_elements] = key
        self.num_elements += 1
        if self.num_elements > 1:
            self.decrease_key(self.num_elements - 1, key)

    def decrease_key(self, index, key):
        self.HeapTree[index] = key
        if index > 0:
            if self.HeapTree[(index - 1) // 2] > key:
                self.HeapTree[index] = self.HeapTree[(index - 1) // 2]
                self.HeapTree[(index - 1) // 2] = key
                self.decrease_key((index - 1) // 2, key)
    def extract_min(self):
        self.HeapTree[0] = self.HeapTree[self.num_elements-1]
        self.HeapTree[self.num_elements - 1] = None
        self.num_elements -= 1
        self.heapify(0)


    def heapify(self, index):
        key = self.HeapTree[index]
        if index*2 + 1 < self.num_elements:
            if self.HeapTree[index*2 + 1] is not None:
                smallest = self.HeapTree[index*2+1]
                if self.HeapTree[index*2+2] is not None and smallest > self.HeapTree[index*2+2]:
                    self.HeapTree[index] = self.HeapTree[index*2+2]
                    self.HeapTree[index*2+2] = key
                    self.heapify(index * 2 + 2)
                else:
                    self.HeapTree[index] = smallest
                    self.HeapTree[index*2+1] = key
                    self.heapify(index * 2 + 1)

