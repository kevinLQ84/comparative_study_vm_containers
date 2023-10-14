import test_runtime
import sys, random, copy

'''
File containing sorting algorithms and evaluation functions
Mergesort
Quicksort
    Lomuto Quicksort
    Hoare Quicksort
Insertion Sort
Heapsort
Selection Sort
Bubble Sort
'''

#region     Mergesorts

# merge uses 2 existing lists and modifies an existing list
def merge(list1, list2, mylist):
        # f1 and f2 represent index counts
        f1 = 0
        f2 = 0

        # checks if iteration over entire list has been done yet
        # if these indexes exceed list size, then we're done
        while f1 + f2 < len(mylist):
            if f1 == len(list1):
                # assign value to replace new index
                mylist[f1+f2] = list2[f2]
                # move index of list 2 by 1
                f2 += 1
            elif f2 == len(list2):
                mylist[f1+f2] = list1[f1]
                # move index of list 1 by 1
                f1 += 1
            elif list2[f2] < list1[f1]:
                # assign value to replace new index
                mylist[f1+f2] = list2[f2]
                # move index of list 2 by 1
                f2 += 1
            else: #list2[f1] < list1[f2]
                # assign value to replace new index
                mylist[f1+f2] = list1[f1]
                # move index of list 1 by 1
                f1 += 1 

def Mergesort(mylist):
    n = len(mylist)
    if n > 1:
        # sort once list is size greater than 1

        # slice list. start at 0 and end at n//2
        list1 = mylist[:n//2]

        # slice list. start at n//2 and end at end of list
        list2 = mylist[n//2:]


        Mergesort(list1)
        Mergesort(list2)
        merge(list1, list2, mylist)
    #return mylist

# test for values 35, 37, 41, 62, 27, 29, 39, 54
# should output 27, 29, 35, 37, 39, 41, 54, 62

# mergeList = [35, 37, 41, 62, 27, 29, 39, 54]
# print(f"Normal Mergesort: {mergesort(mergeList)}")


#endregion

#region     Lomuto Quicksort
'''
#choose last item of list as a "pivot"
step through list from start of list
    remember the earliest position of an item greater than the pivot
keep iterating
when an item less than or equal to pivot is found, swap with the earliest item
advance until last item is swapped
there are now sub lists

to not use list slicing, just don't use python slicing and handle the indexes
    by operating on the same list

need repeated calls and only finishes once the 1st list's pivot reaches the start
2nd sub list needs it's own pivot to reach the start
'''

'''
notes
need to form 2 sub lists, pass on inside another function
sub lists need to remain inside the same list, manage ONLY INDEXES
the additional function needs to be inside of the parent so the list is maintained and
    new lists are not created
return only when the start and pivot values end up being the same
'''

def Lomuto_Quicksort(mylist, start = 0, end = None):
    # if list input is just the list
    if end == None:
        end = len(mylist)-1
        
    # as long as the partition is greater than 1
    if start < end:
        pivot = end
        pointer = start
        # disregard last pivot element as that will be swapped anyways
        for i in range(start, end):
            # if an item is less than the pivot
            if mylist[i] <= mylist[pivot]:
                # swap with the earliest larger item
                # if there is no earliest largest item, then it swaps with itself
                mylist[i], mylist[pointer] = mylist[pointer], mylist[i]
                # after a swap, increment the pointer to look at the next item
                pointer+=1
                # if there is no larger item, the pointer merely keeps up with i
                # if there is a larger item, the pointer will remember it
                # i would increment while the pointer stays on the item
        # after the loop, the pivot swaps with the pointer
        # the pointer acts as a split for subsequent sorts
        # if no larger element is found, the pivot essentially swaps with itslf
        mylist[pointer], mylist[pivot] = mylist[pivot], mylist[pointer]

        # use recursion
        Lomuto_Quicksort(mylist, start, pointer-1)
        Lomuto_Quicksort(mylist, pointer+1, end)

        #return mylist
    
#endregion

#region     Bottom up Mergesort
'''
Implement the bottom-up version of Mergesort,
that uses an additional list (i.e. O(n) space). 

'''
def mergeBU(mylist, otherlist, start, middle, end):
    # f1 and f2 represent index counts
    f1 = start
    f2 = middle
    new_index = start
    
    # checks if iteration over entire list has been done yet
    # if these indexes exceed limit, then we're done
    while new_index < end:
        if f1 == middle:
            # assign value to replace new index
            otherlist[new_index] = mylist[f2]
            # move index of list 2 by 1
            f2 += 1
        elif f2 == end:
            otherlist[new_index] = mylist[f1]
            # move index of list 1 by 1
            f1 += 1
        elif mylist[f2] < mylist[f1]:
            # assign value to replace new index
            otherlist[new_index] = mylist[f2]
            # move index of list 2 by 1
            f2 += 1
        else: #list2[f1] < list1[f2]
            # assign value to replace new index
            otherlist[new_index] = mylist[f1]
            # move index of list 1 by 1
            f1 += 1

        new_index+=1
    

def BU_Mergesort(mylist, otherlist = None):
    # listsize represents size of sublists of iteration
    length = len(mylist)

    # generate empty list to copy into
    if otherlist == None:
        otherlist = [None]*length

    listsize = 1
    # as long as partitions dont exceed/equal size of list itself
    while listsize < length:
        # listsize*2 represens total length of a list split into 2
        for start in range(0, length, listsize*2):
            # start already defined

            # middle can exceed list size
            middle = min(start+listsize, length)
            # end can exceed list size
            end = min(start+listsize*2, length)
            mergeBU(mylist, otherlist, start, middle, end)
        # once a ful merge is finished, copy the sorted iteration of otherlist
        mylist, otherlist = otherlist, mylist

        # increase list size per partition
        listsize*=2

    #return mylist
#endregion

#region     Hoare Quicksort
'''
pivot is at the start of list
two indexes that start at two ends
move toward each other
find a larger value on the left side and lesser value on the right side
then swap and swap the pivot with the smaller index after the swap
the indexes do not change after this swap

need a partition first
'''

# should be able to not require a child function to modify the list in-place
# re-use the partition each time
def Hoare_QS_Partition(mylist, start, end):
    pivot = start
    # pointers point to large and small
    l_pointer = start
    r_pointer = end

    # as long as pivot isn't returned
    # continue iteration from start and end points
    # they will be modified on subsequent iterations once a swap is made
    while True:

        # # find larger left
        # for i in range(start, end+1):
        #     if mylist[pivot] < mylist[i]:
        #         # if an item is larger, record index of it
        #         l_pointer = i
        #         break
        
        
        # # find smaller right
        # for j in range(end, start-1, -1):
        #     if mylist[pivot] >= mylist[j]:
        #         # if an item is smaller, record index of it
        #         r_pointer = j
        #         break

        while l_pointer <= end:
            if mylist[pivot] < mylist[l_pointer]:
                break
            else:
                l_pointer+=1
        
        while r_pointer >= start:
            if mylist[pivot] >= mylist[r_pointer]:
                break
            else:
                r_pointer-=1
        
        # if no larger left or right is found, swap will be made with start and end values
        # this would immediately trigger the return when the pivot has changed indexes
        
        # if pointers exceed eachother after swap check
        # swap pivot to right pointer and return it
        # will be used to find end of next partitions
        if l_pointer >= r_pointer:
            mylist[pivot], mylist[r_pointer] = mylist[r_pointer], mylist[pivot]
            # return only used properly once to identify 1st partition point
            return r_pointer
        
        # swap
        mylist[l_pointer], mylist[r_pointer] = mylist[r_pointer], mylist[l_pointer]

        # if left pointer is still at the start
        # pivot has already moved after swap
        if l_pointer == start:
            return r_pointer
        

        # set new starts and ends
        start = l_pointer
        end = r_pointer

        

def Hoare_Quicksort(mylist, start = None, end = None):
    # if indexes are not initialised, do that
    # assumes partitions not made
    if start == None and end == None:
        start = 0
        end = len(mylist)-1

    # check if the start has exceeded or become the end
    # this means a partitioned list is finished
    if start < end:

        # perform a partition
        split = Hoare_QS_Partition(mylist, start, end)

        # first half
        Hoare_Quicksort(mylist, start, split-1)

        # second half
        Hoare_Quicksort(mylist, split+1, end)
    
    #return mylist

# h_list = [41, 37, 35, 62, 29, 39, 54, 27, 60, 25, 40, 56, 51, 48, 43, 51, 43]
# h_list = [10, 7, 8, 9, 1, 5]
# Hoare_Quicksort(h_list)
# print(f"Hoare Quicksort: {h_list}")



    
    


#endregion

#region     Insertion sort
def Insertion_Sort(mylist):
    n = len(mylist)
    i = 1
    # while index 1 and beyond is less than the last index of the list
    # iterate through index 1 to last index
    while i < n:
        # j represents item before item i, the one we point to during iteration
        j = i-1
        # as long as item i is lesser than j and j is >= 0, index j is lowered
        # if j ends up always being larger, then item i swaps the first item in the list
        while mylist[i] < mylist[j] and j > -1:
            j -= 1
        # insert i in the cell after j
        # temp holds the current pointer item
        temp = mylist[i]
        # k is the index 1 down
        k = i-1
        # while loop to seemingly swap each element with one index higher until j is reached
        while k > j:
            mylist[k+1] = mylist[k]
            k -= 1
            # restore k pointer + 1 index and replace item there with the current pointer item
        mylist[k+1] = temp
        # shift pointer index up by 1
        i += 1
    #return mylist

#endregion

#region     Heapsort
def binary_heapify(mylist:list, length = 0):
    # given a list, use a for loop with list splicing
    for i in range(1,length):
        # create temp value to hold index and move pointer up to repeatedly check parents
        j = i
        while j != 0:
            # parent calculation of heap
            # will need to keep swapping in order to see if parent remains larger than children
            parent = (j-1)//2
            # if currently pointed child is larger than parent
            if mylist[j] > mylist[parent]:
                # swap parent and child
                mylist[j], mylist[parent] = mylist[parent], mylist[j]
                # change j to parent index value and now check the swapped element with it's own parent
                j = parent
            else:
                # if no swap is required, skip and end the current comparison
                # also end if next element to check is 1st index
                j = 0 

    #return mylist

def Heapsort(mylist):
    length = len(mylist)
    full_length = len(mylist)
    # heapify current length of list. do this once
    binary_heapify(mylist, length)
    # now a max heap is made

    # swap last and first index, then bubble down the swapped element to it's correct place
    while length > 0:
        # once heapified, swap first and last of the list
        # eventually the list will be sorted from lowest to highest
        # after swap, parent node at first can have incorrect children
        # bubble down until children are greater than parent
        mylist[0], mylist[length-1] = mylist[length-1], mylist[0]
        # reduce the length by 1, ignoring swapped end of list
        length -= 1

        parent = 0
        # break loop once in place properly
        while True:
            larger_child = None

            # account for potential list out of index error
            l_child = 2*parent + 1
            r_child = 2*parent + 2

            # parent has to be larger than child
            # swap once the parent ends up lesser than the child

            # if both children don't exist, stop
            if l_child >= length and r_child >= length:
                break

            # if only right child
            if l_child >= length:
                larger_child = r_child
            # if only left child
            elif r_child >= length:
                larger_child = l_child
            
            # if both children exist
            else:
                if mylist[l_child] > mylist[r_child]:
                    larger_child = l_child
                else:
                    larger_child = r_child

            if larger_child != None:
                if mylist[parent] < mylist[larger_child]:
                    mylist[parent], mylist[larger_child] = mylist[larger_child], mylist[parent]
                    parent = larger_child
                    continue

            # if no swaps occur, end loop
            break

    #return mylist
#endregion

#region     Selection Sort

def Selection_Sort(mylist):
    j = 0
    length = len(mylist)
    while j < length-1:
        lowest = j
        # find lowest of iteration of list
        for i in range(j, length):
            if mylist[i] < mylist[lowest]:
                lowest = i

        # swap with lowest in iteration
        mylist[j], mylist[lowest] = mylist[lowest], mylist[j]
        # increment j to the next index
        j += 1
    #return mylist

#endregion

#region     Bubble Sort

# bubble sort
def Bubble_Sort(mylist):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(len(mylist)-1):
            # check next item, swap if not right
            if mylist[i] > mylist[i+1]:
                sorted = False
                # swap if previous is larger
                mylist[i], mylist[i+1] = mylist[i+1], mylist[i]
    
    #return mylist

#endregion

#region     Sorted List Check
'''
check if a list is actually sorted
as long as the next element of the current one is in-place, then it's sorted
'''
def check_sorted(function, input) -> bool:
    array = function(input)
    for i in range(len(array)-1):
            if array[i] > array[i+1]:
                return False
    return True

# control function to test check_sorted
def bingus_sort(array):
    # return the array given
    pass
    #return array

#endregion

#region     list evaluation functions
'''
Since all functions in this file take an input from a list, these only generate lists.
'''
def randomlistgen(n, k = 0, unsort_shuffling = True, partial_sort: int = 0):
    '''
    Generates a list of random numbers using random.shuffle.
    '''
    # n is size
    # k is duplicates
    # set checks for invalid input
    if k >= n:
        raise ValueError("Duplicates are greater than list size")
    
    full_size = n-k
    randlist: list = list(range(1, full_size+1))

    for i in range(k):
        # append duplicates
        randlist.append(random.choice(randlist))
    
    if unsort_shuffling:
        random.shuffle(randlist)
    else:
        randlist.sort()
        # parital sorting will only occur when the list is sorted
        # and the partial sort num is > 0
        swaps = int(n//partial_sort)
        if partial_sort > 0:
            for i in range(swaps):
                item = random.randrange(0, n-2)
                randlist[item], randlist[item+1] = randlist[item+1], randlist[item] 

    return randlist
    
def evaluate(n, k, num, function, unsort_shuffling = True, partial_sort = 0):
    # create container for num of lists to be used
    lists = []

    for i in range(num):
        lists.append(randomlistgen(n, k, unsort_shuffling, partial_sort))
    
    average: float = 0

    for list_item in lists:
        average += (test_runtime.time_test(function, list_item))
    
    average/=num

    return average
    
def evaluate_all(n, k, num, functions: list, unsort_shuffling = True, partial_sort = 0):
    if unsort_shuffling == True or partial_sort <= 0:
        initial_sorting = "Initially Sorted"
    elif unsort_shuffling == False and partial_sort > 0:
        initial_sorting = "Partially Sorted"

    print(f"List size: {n}       Duplicates: {k}        {initial_sorting}: {not unsort_shuffling}\n")
    # container should contain all desired functions to test
    # make sure to reset tested lists
    lists = []
    for i in range(num):
        lists.append(randomlistgen(n, k, unsort_shuffling, partial_sort))

    for function in functions:

        # set up base arguments required for input
        lists_copy = copy.deepcopy(lists) # guarantee a true copy of a list rather than a pointer
        average: float = 0

        # get the average
        for list_item in lists_copy:
                average += (test_runtime.time_test(function, list_item))
        average/=num
        print(f"{function.__name__}: {average} seconds")
    print()

def evalautescale():
    '''
    evaluates a set of defined functions within this function
    '''
    # implement failsafes if list sizes too big for On^2
    parameters = [(100, 20),
                  (1000, 200),
                  (10000, 2000),
                  (100000, 20000)]
    functions = [#Insertion_Sort,\
                 Heapsort, Mergesort, \
                 BU_Mergesort, Hoare_Quicksort, Lomuto_Quicksort, bingus_sort]
    for (n,k) in parameters:
        evaluate_all(n,k,20,functions)

#endregion

#region     driver code for showing runtimes
def sorting_runtime_comparison(size, duplicates, sorted: bool, \
                               recursion_limit = 1000, check = False, rseed = None):
    
    # set checks for invalid input
    if duplicates >= size:
        return
    
    # set a seed for random if needed
    # will override list generation
    if rseed != None:
        random.seed(rseed)
    
    # set recursion limit
    sys.setrecursionlimit(recursion_limit)
    
    full_size = size - duplicates

    randlist = random.sample(range(0, full_size), full_size)

    for i in range(duplicates):
        randlist.append(random.choice(randlist))

    if sorted:
        randlist.sort()
    else:
        random.shuffle(randlist)

    print(f"List size: {size}       Duplicates: {duplicates}        Intially Sorted: {sorted}\n")
    
    # ensure each array argument is not pointing to same memory location
    functions = [Bubble_Sort, Selection_Sort, Insertion_Sort, Heapsort, Mergesort, \
                 BU_Mergesort, Hoare_Quicksort, Lomuto_Quicksort, bingus_sort]
    for algorithm in functions:
        reset_list = randlist.copy()

        if check:
            print(f"\nSuccessful Sort: {check_sorted(algorithm, reset_list)}")  # check if list is actually sorted
            reset_list = randlist.copy()
        
        test_runtime.time_test(algorithm, reset_list, prints = True)
    print()
#endregion

# testing runtime of functions within file
if __name__ == "__main__":
    sys.setrecursionlimit(2500)
    # sorting_runtime_comparison(1000, 200, False, 2500, rseed=10)
    functs = [ Heapsort, Mergesort, \
                 BU_Mergesort, Hoare_Quicksort, Lomuto_Quicksort, bingus_sort]
    #evaluate_all(6000, 100, 25, functs)

    evalautescale()
    
    '''
    note
    Lomuto is a little worse on a partially sorted list with n^2 swaps than Hoare
    '''
    
    