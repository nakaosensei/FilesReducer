latitude = 0
longitude = 1
latRange = 0.0001
longRange = 0.0001


def getModule(number):
    if number<0:
        return number*-1
    return number

def merge(llist, rlist):
    """
    Merge two lists into an ordered list.
    """
    final = []
    while llist or rlist:
        # This verification is necessary for not try to compare
        # a NoneType with a valid type.
        if len(llist) and len(rlist):
            print(llist[0][latitude])
            print(llist[0][longitude])
            print(rlist[0][latitude])
            print(rlist[0][longitude])

            lmLat = getModule(llist[0][latitude])
            lmLong = getModule(llist[0][longitude])
            rmLat = getModule(rlist[0][latitude])
            rmLong = getModule(rlist[0][longitude])
            latDiff = getModule(lmLat-rmLat)
            longDiff = getModule(lmLong-rmLong)


            if llist[0][latitude] < rlist[0][latitude] and llist[0][longitude] < rlist[0][longitude] and latDiff<latRange and longDiff<longRange:
                final.append(llist.pop(0))
            else:
                final.append(rlist.pop(0))

        # This two conditionals here, is for the case when the two lists
        # have diferent sizes. This save us of an error trying to acess
        # an index out of range.
        if not len(llist):
            if len(rlist): final.append(rlist.pop(0))

        if not len(rlist):
            if len(llist): final.append(llist.pop(0))

    return final


def merge_sort(list):
    """
    Sort the list passed by argument with merge.
    """
    if len(list) < 2: return list
    mid = int(len(list) / 2)
    return merge(merge_sort(list[:mid]), merge_sort(list[mid:]))