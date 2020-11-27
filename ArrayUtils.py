def crossDivideStoreList(storeList):
   newLists = []
   for i in range(0,len(storeList)):
       toRemove = []
       for j in range(0,len(storeList)):
           if i!=j:
               toRemove.append(storeList[j])
       newLists.append(toRemove)
   return newLists

def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs

def splitDictEqually(input_dict, chunks=2):
    "Splits dict by keys. Returns a list of dictionaries."
    # prep with empty dicts
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k in input_dict.keys():
        return_list[idx][k] = input_dict[k]
        if idx < chunks-1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list

#def splitArrayInNChunks(input_array, chunks):
#   return [input_array[i:i+int(chunks)] for i in range(0 , (chunks-1)*int(chunks), int(chunks))]

def splitArrayInNChunks(input_array, chunks):
    qtdeElementsPerChunk=None
    if(chunks>=len(input_array)):
        qtdeElementsPerChunk=1
    else:
        qtdeElementsPerChunk= int(len(input_array)/chunks)
    outPut = []
    chunk = []
    for i in range(0, len(input_array)):
        if len(chunk)<qtdeElementsPerChunk:
            chunk.append(input_array[i])
        else:
            outPut.append(chunk)
            chunk = []
            chunk.append(input_array[i])
    if len(chunk)>0:
        if len(outPut)>0:
            for element in chunk:
                outPut[len(outPut)-1].append(element)
        else:
            outPut.append(chunk)
    return outPut

