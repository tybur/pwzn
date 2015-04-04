# Written by Magnus Lie Hetland
# modified to utilize Cython
# cython: profile=True
# filename: zadanie1.pyx

import cython
from cpython cimport array as c_array
from array import array

"Everybody's favourite sorting algorithm... :)"

cpdef int partition(int[:] l, int start, int end):
    cdef int pivot = l[end]                          # Partition around the last value
    cdef int bottom = start-1                           # Start outside the area to be partitioned
    cdef int top = end                                  # Ditto

    cdef int done = 0
    while done == 0:                            # Until all elements are partitioned...

        while done == 0:                        # Until we find an out of place element...
            bottom = bottom+1                  # ... move the bottom up.

            if bottom == top:                  # If we hit the top...
                done = 1                       # ... we are done.
                break

            if l[bottom] > pivot:           # Is the bottom out of place?
                l[top] = l[bottom]       # Then put it at the top...
                break                          # ... and start searching from the top.

        while done == 0:                        # Until we find an out of place element...
            top = top-1                        # ... move the top down.

            if top == bottom:                  # If we hit the bottom...
                done = 1                       # ... we are done.
                break

            if l[top] < pivot:              # Is the top out of place?
                l[bottom] = l[top]       # Then put it at the bottom...
                break                          # ...and start searching from the bottom.

    l[top] = pivot                          # Put the pivot in its place.
    return top                                 # Return the split point


cpdef int quicksort(int[:] l, int start, int end):
    cdef int split = 0
    if start < end:                            # If there are two or more elements...
        split = partition(l, start, end)    # ... partition the sublist...
        quicksort(l, start, split-1)        # ... and sort both halves.
        quicksort(l, split+1, end)
    else:
        return 0

def qs(l, start, end):
    cdef c_array.array la = array('i', l)
    cdef int[:] lv = la
    cdef int st = start
    cdef int e = end
    quicksort(lv, st, e)
    return la
