

def  melon_count(boxes, melons):
    max_num = 0
    cur_num = 0
    box_ind = 0
    box_num = len(boxes)
    for i in range(len(melons)):
        # get one melon from list, try to put it into a box
        while box_ind < box_num:
            if melons[i] <= boxes[box_ind]:
                cur_num += 1    # cur list + 1
                box_ind += 1    # go to the next box
                break
            else:
                box_ind += 1    # go to the next box
        if box_ind == box_num:
            # means all boxes have been tried
            max_num = max(max_num, cur_num)
            cur_num = 0     # initial the cur sum number
            box_ind = 0     # initial the box index
    return max_num

#print melon_count([4, 3,2,1], [1,2,2,1, 5])

import math
def dist(a, b):
    return math.sqrt(pow(a[0]-b[0], 2) + pow(a[1]-b[1], 2) + pow(a[2]-b[2], 2))

def closestColor(pixels):
    for pixel in pixels:
        # convert the color into decimal numbers
        r = int(pixel[0:8], 2)
        g = int(pixel[8:16], 2)
        b = int(pixel[16:], 2)
        pixel_color = [r, g, b]
        # find the closest color
        min_dist = 10000
        close_color = ''
        if min_dist >= dist(pixel_color, [0,0,0]):
            min_dist = dist(pixel_color, [0,0,0])
            close_color = 'Red'
        if min_dist >= dist(pixel_color, [0,0,0]):
            min_dist = dist(pixel_color, [0,0,0])
            close_color = 'Red'
        if min_dist >= dist(pixel_color, [0,0,0]):
            min_dist = dist(pixel_color, [0,0,0])
            close_color = 'Red'
        if min_dist >= dist(pixel_color, [0,0,0]):
            min_dist = dist(pixel_color, [0,0,0])
            close_color = 'Red'
        if min_dist >= dist(pixel_color, [0,0,0]):
            min_dist = dist(pixel_color, [0,0,0])
            close_color = 'Red'

closestColor(['101010101010101010101010'])


def cutSticks(lengths):
    cut_list = []
    while len(lengths)>1:
        cut_list.append(len(lengths))
        lengths = sorted(lengths)
        new_lengths = []
        for length in lengths:
            new_length = length - lengths[0]
            if new_length > 0:
                new_lengths.append(new_length)
        lengths = new_lengths
    cut_list.append(len(lengths))
    return cut_list

print cutSticks([1,2,3,4,3,3,2,1])