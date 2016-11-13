'''
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity
should be O(log (m+n)).

Example 1:
nums1 = [1, 3]
nums2 = [2]

The median is 2.0

Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5
'''


def get_min(array, i, num):
    if i == len(array):
        return []
    else:
        return array[i:i + num]


class Solution(object):

    def findMedianSortedArrays(self, nums1, nums2):
        '''
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        '''
        num_elems = len(nums1) + len(nums2)
        num_to_skip = num_elems / 2
        if num_elems % 2 == 0:
            num_to_skip -= 1
        i = 0
        j = 0
        while i + j < num_to_skip:
            num_left = num_to_skip - i - j
            # d is the minimum number of smallest elements that we can safely
            # discard from either of the arrays
            if num_left == 1:
                d = 1
            else:
                d = num_left / 2

            # Is one of the arrays depleted?
            if i == len(nums1):
                j += d
            elif j == len(nums2):
                i += d
            else:
                d = min(d, len(nums1) - i, len(nums2) - j)
                assert d
                if nums1[i + d - 1] < nums2[j + d - 1]:
                    i += d
                else:
                    j += d

        if num_elems % 2:
            mins = get_min(nums1, i, 1)
            mins.extend(get_min(nums2, j, 1))
            mins.sort()
            return float(mins[0])
        else:
            # We need average of two minimum elements so just plop first two
            # of both, sort and return mean of the first two sorted ones
            mins = get_min(nums1, i, 2)
            mins.extend(get_min(nums2, j, 2))
            mins.sort()
            return float(sum(mins[:2])) / 2


if __name__ == '__main__':
    s = Solution()

    assert s.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert s.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    assert s.findMedianSortedArrays([1], [2, 3, 4, 5, 6, 7, 8, 9]) == 5.0
