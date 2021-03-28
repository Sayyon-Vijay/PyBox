from operator import attrgetter

list1 = [[6, "1"], [1, "2"], [9, "3"], [4, "4"], [7, "5"], [3, "6"]]

def active(list1):
    r = 1

    sorted_list1 = sorted(list1, key=attrgetter([1]))



    active_list = []

    L = []

    for i in sorted_list1:
        L.append([i[0] - r, i[0] + r, i[1]])


    for i in L:
        if L.index(i) != len(L) - 1:
            if i[1] > L[L.index(i) + 1][0]:
                active_list.append(i)
                active_list.append(L[L.index(i) + 1])

    print(active_list)

sorted_list1 = sorted(list1, key=attrgetter("[1]"))

print(sorted_list1)

[[0, 2], [2, 4], [3, 5], [5, 7], [6, 8], [8, 10]]