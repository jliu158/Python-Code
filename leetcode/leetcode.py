def pascal_triangle(numRows):
    row = [1]
    final_row = [row]
    while numRows > 1:
        row1 = row + [0]
        row2 = [0] + row
        row = []
        for i in range(len(row1)):
            row.append(row1[i] + row2[i])
        numRows -= 1
        final_row.append(row)
    return final_row


#print(pascal_triangle(10))



def lengthOfLongestSubstring(s):
    max_ = ''
    if len(set(s)) == 0:
        return 0
    else:
        substr = ''
        for i in s:
            if i in substr:
                n = substr.index(i)
                if len(substr) > len(max_):
                    max_ = substr
                substr = substr[n+1:]+i
            else:
                substr += i
                if len(substr) > len(max_):
                    max_ = substr
    return len(max_)


#print(lengthOfLongestSubstring('abcda'))



def findMedianSortedArrays(num1, num2):
    i = 0
    j = 0
    whole = len(num1)+len(num2)
    if whole%2 == 0:
        med = whole/2
        med_1 = 0
        med_2 = 0
        while i+j < med+1:
            print(i,j)
            if num1[i]>num2[j]:
                med_1, med_2 = num2[j], num1[i]
                i += 1
            elif num1[i]<num2[j]:
                med_1, med_2 = num1[i], num2[j]
                j += 1
        return (med_1+med_2)/2

    else:
        med = (whole+1)/2
        med_ = 0
        while i+j < med+3:
            if num1[i]>num2[j]:
                med_ = num1[i]
                i += 1
            elif num1[i]<num2[j]:
                med_ = num2[j]
                j += 1
        return med_


print(findMedianSortedArrays([1,2],[3,4]))
