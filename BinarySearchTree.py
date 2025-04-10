import random
import sys
from time import perf_counter
from BSTNode import BSTNode


class BST:
    # Constructor that initializes the root to nothing (empty bst)
    def __init__(self):
        self.root = None

    # insert method that either adds the first element of the bst, or calls a helper method that places the element
    # where it has to go
    def insert(self, new_data):
        new_node = BSTNode(new_data)
        if self.root is None:
            self.root = new_node
        else:
            self.insertNode(new_node, self.root)

    # helper method that recursively adds element to its proper place
    def insertNode(self, new_node, subroot):

        if new_node.data < subroot.data:
            if subroot.left is None:
                subroot.left = new_node
            else:
                self.insertNode(new_node, subroot.left)
        else:
            if subroot.right is None:
                subroot.right = new_node
            else:
                self.insertNode(new_node, subroot.right)

    # takes the key from the user and calls helper method
    def searchRecursively(self, key):
        return self.searchRecHelper(key, self.root)

    # helper method recursively searches according to rules of bst
    def searchRecHelper(self, key, subroot):
        if key == subroot.data:
            return subroot.data
        elif key < subroot.data:
            return self.searchRecHelper(key, subroot.left)
        else:
            return self.searchRecHelper(key, subroot.right)

    def searchLoop(self, key):
        subroot = self.root

        while subroot.data is not None and subroot.data is not key:
            if key < subroot.data:
                subroot = subroot.left
            else:
                subroot = subroot.right

        return subroot.data

    def findmin(self):
        if self.root is None:
            return None
        else:
            return self.findminhelper(self.root).data

    def findminhelper(self, subroot):
        if subroot.left is None:
            return subroot
        else:
            return self.findminhelper(subroot.left)

    def preorderwalk(self):
        self.preorderwalkrec(self.root)

    def preorderwalkrec(self, subroot):
        print(subroot.data)
        if subroot.left is not None:
            self.preorderwalkrec(subroot.left)
        if subroot.right is not None:
            self.preorderwalkrec(subroot.right)

    def postorderwalk(self):
        self.postorderwalkrec(self.root)

    def postorderwalkrec(self, subroot):
        if subroot.left is not None:
            self.postorderwalkrec(subroot.left)
        if subroot.right is not None:
            self.postorderwalkrec(subroot.right)
        print(subroot.data)


if __name__ == '__main__':
    testTree = BST()
    list = []
    # Creates a random tree of 100 nodes
    for i in range(100):
        rand = random.randint(1, 100)
        testTree.insert(rand)
        list.append(rand)
    # Makes a short tree i can track to validate post and pre order walks
    # testTree.insert(4)
    # list.append(4)
    # testTree.insert(2)
    # list.append(2)
    # testTree.insert(6)
    # list.append(6)
    # testTree.insert(1)
    # list.append(1)
    # testTree.insert(3)
    # list.append(3)
    # testTree.insert(5)
    # list.append(5)
    # testTree.insert(7)
    # list.append(7)

    # Returns run time of recursive search
    totalTime = 0
    for number in list:
        start = perf_counter()
        testTree.searchRecursively(number)
        end = perf_counter()
        elapsed_time = end - start
        totalTime += elapsed_time
    print(totalTime / (len(list)))
    # Returns run time of loop search
    totalTime = 0
    for number in list:
        start = perf_counter()
        testTree.searchLoop(number)
        end = perf_counter()
        elapsed_time = end - start
        totalTime += elapsed_time
    print(totalTime / (len(list)))

    # Pre and postorder walks
    testTree.preorderwalk()
    testTree.postorderwalk()

    # Prints minimum
    print(testTree.findmin())
