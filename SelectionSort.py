

def selectionSort(list):

    for i in range(len(list)-1):
        min = i
        for j in range(1, len(list)-1):
            if list[min] > list[j]:
                min = j

        temp = list[min]
        list[min] = list[i]
        list[i] = temp

    print(list)

if __name__ == '__main__':
    list = [5, 3, 10, 5, 2]
    selectionSort(list)