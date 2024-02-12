# Step 1
import string
import copy
import math
alphabet = list(string.ascii_lowercase)
# Finds the number of qubits
txtFile = input("File name: ")
file_in = open(f"{txtFile}copycopy", "r+")
lines = file_in.readlines()
qbitnum = 0
oneQubitGates = 0
lenBefore = 0
lenAfter = 0
twoQubitGates = 0
for line in lines:
    if 'qreg' in line:
        qbitnum += 1
# Creates lists for all qubits
assert qbitnum <= 26
allGates = {var: [] for var in string.ascii_lowercase[:qbitnum]}
beforeGates = {var: [] for var in string.ascii_lowercase[:qbitnum]}
# Finds the start line
start = 0
smth = 0
for line in lines:
    smth += 1
    if 'creg' in line:
        start = smth + 1
        break


# Finds the duplicate index
def list_duplicates_of(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
# List consisting only of gates
onlyGates = []
for o in range(start - 1, len(lines)):
    onlyGates.append(lines[o])
    if 'measure' in lines[o]:
        onlyGates.remove(onlyGates[len(onlyGates) - 1])
        break
# Divides all gates
uuu = 0
source = None
letterBefore = None
ancIndex = None
ancLetter = None
for Line in range(len(lines)):
    if "qreg ancilla0" in lines[Line]:
        letterBefore = lines[Line - 1][5]


for gate in range(len(onlyGates)):
    source = onlyGates[gate]
    braket = list_duplicates_of(source, '[')
    if len(braket) == 1:
        letter = source[braket[0] - 1]
        letterNum = braket[0] - 1
        gateEnd = letterNum - 1
        gateName = ''
        for idx in range(0, gateEnd):
            gateName = gateName + source[idx]
        for element in range(qbitnum):
            if letter == alphabet[element]:
                allGates[alphabet[element]].append(gateName)
                beforeGates[alphabet[element]].append(gateName)

    if len(braket) == 2:
        var1 = source[braket[0] - 1]
        varNum = braket[0] - 1
        var2 = source[braket[1] - 1]
        gateName = ''
        for idx in range(0, varNum - 1):
            gateName = gateName + source[idx]
        for element in range(qbitnum):
            if var1 == alphabet[element]:
                allGates[alphabet[element]].append("control")
                beforeGates[alphabet[element]].append("control")
            if var2 == alphabet[element]:
                allGates[alphabet[element]].append("target")
                beforeGates[alphabet[element]].append("target")



# Step 2: array of all sqg's by qubits
singleGates = {var: [] for var in string.ascii_lowercase[:qbitnum]}

for gate in range(len(onlyGates)):
    source = onlyGates[gate]
    braket = list_duplicates_of(source, '[')
    if len(braket) == 1:
        letter = source[braket[0] - 1]
        letterNum = braket[0] - 1
        gateEnd = letterNum - 1
        gateName = ''
        for idx in range(0, gateEnd):
            gateName = gateName + source[idx]
        for element in range(qbitnum):
            if letter == alphabet[element]:
                if gateName == "h" or "x" or "s" or "tdg" or "sdg":
                    singleGates[alphabet[element]].append(gateName)
singleGatesNum = {var: [] for var in alphabet[:qbitnum]}

for x in range(qbitnum):
    qubit = singleGates[alphabet[x]]
    for i, v in enumerate(qubit):
        totalcount = qubit.count(v)
        count = qubit[:i].count(v)
        singleGatesNum[alphabet[x]].append(v + str(count + 1) if totalcount > 1 else v)

pairs = {var: [] for var in alphabet[:qbitnum]}

if len(singleGatesNum) > 1:
    for z in range(qbitnum):
        for o in range(len(singleGatesNum[alphabet[z]]) - 1):
            pairs[alphabet[z]].append([singleGatesNum[alphabet[z]][o], singleGatesNum[alphabet[z]][o + 1]])

allGatesNum = {var: [] for var in alphabet[:qbitnum]}

for x in range(qbitnum):
    qubit = allGates[alphabet[x]]
    for i, v in enumerate(qubit):
        totalcount = qubit.count(v)
        count = qubit[:i].count(v)
        allGatesNum[alphabet[x]].append(v + str(count + 1) if totalcount > 1 else v)

pairsCopy: dict = copy.deepcopy(pairs)
distancePriority = {var: [] for var in alphabet[:qbitnum]}

distanceCopy = {var: [] for var in alphabet[:qbitnum]}

# Removes immovable gates

for x in range(qbitnum):
    for z in range(len(pairs[alphabet[x]])):
        index1 = allGatesNum[alphabet[x]].index(pairs[alphabet[x]][z][0])
        index2 = allGatesNum[alphabet[x]].index(pairs[alphabet[x]][z][1])
        distance = index2 - index1
        mobility1 = 0
        mobility2 = 0
        for hhh in range(distance - 1):
            if 'h' in allGatesNum[alphabet[x]][index1]:
                if 'target' in allGatesNum[alphabet[x]][index1 + hhh + 1]:
                    mobility1 += 1
                else:
                    break
            elif 'x' in allGatesNum[alphabet[x]][index1]:
                if 'target' in allGatesNum[alphabet[x]][index1 + hhh + 1]:
                    mobility1 += 1
                else:
                    break
            elif 't' in allGatesNum[alphabet[x]][index1]:
                if 'control' in allGatesNum[alphabet[x]][index1 + hhh + 1]:
                    mobility1 += 1
                else:
                    break
            elif 's' in allGatesNum[alphabet[x]][index1]:
                if 'control' in allGatesNum[alphabet[x]][index1 + hhh + 1]:
                    mobility1 += 1
                else:
                    break
            elif 'tdg' in allGatesNum[alphabet[x]][index1]:
                if 'control' in allGatesNum[alphabet[x]][index1 + hhh + 1]:
                    mobility1 += 1
                else:
                    break
            elif 'sdg' in allGatesNum[alphabet[x]][index1]:
                if 'control' in allGatesNum[alphabet[x]][index1 + hhh + 1]:
                    mobility1 += 1
                else:
                    break
        for u in range(distance - 1):
            if 'h' in allGatesNum[alphabet[x]][index2]:
                if 'target' in allGatesNum[alphabet[x]][index2 - u - 1]:
                    mobility2 += 1
                else:
                    break
            elif 'x' in allGatesNum[alphabet[x]][index2]:
                if 'target' in allGatesNum[alphabet[x]][index2 - u - 1]:
                    mobility2 += 1
                else:
                    break
            elif 't' in allGatesNum[alphabet[x]][index2]:
                if 'control' in allGatesNum[alphabet[x]][index2 - u - 1]:
                    mobility2 += 1
                else:
                    break
            elif 's' in allGatesNum[alphabet[x]][index2]:
                if 'control' in allGatesNum[alphabet[x]][index2 - u - 1]:
                    mobility2 += 1
                else:
                    break
            elif 'tdg' in allGatesNum[alphabet[x]][index2]:
                if 'control' in allGatesNum[alphabet[x]][index2 - u - 1]:
                    mobility2 += 1
                else:
                    break
            elif 'sdg' in allGatesNum[alphabet[x]][index2]:
                if 'control' in allGatesNum[alphabet[x]][index2 - u - 1]:
                    mobility2 += 1
                else:
                    break
        mobility = mobility1 + mobility2
        if distance - mobility > 1:
            pairsCopy[alphabet[x]][z] = "delete"
for x in range(qbitnum):
    for z in reversed(range(len(pairs[alphabet[x]]))):
        if pairsCopy[alphabet[x]][z] == "delete":
            del pairsCopy[alphabet[x]][z]
noListPairs = {var: [] for var in string.ascii_lowercase[:qbitnum]}

for x in range(qbitnum):
    for z in range(len(pairsCopy[alphabet[x]])):
        for y in range(2):
            noListPairs[alphabet[x]].append(pairsCopy[alphabet[x]][z][y])
for x in range(qbitnum):
    for z in range(len(pairsCopy[alphabet[x]])):
        index1 = allGatesNum[alphabet[x]].index(pairs[alphabet[x]][z][0])
        index2 = allGatesNum[alphabet[x]].index(pairs[alphabet[x]][z][1])
        distance = index2 - index1
        distancePriority[alphabet[x]].append([distance, pairsCopy[alphabet[x]][z]])
    distancePriority[alphabet[x]].sort()
for x in range(qbitnum):
    for z in range(len(pairsCopy[alphabet[x]])):
        distanceCopy[alphabet[x]].append(distancePriority[alphabet[x]][z][1])

for x in range(qbitnum):
    for item in range(len(pairsCopy[alphabet[x]])):
        source = noListPairs[alphabet[x]]
        repeat = list_duplicates_of(source, distancePriority[alphabet[x]][item][1][0])
        repeat2 = list_duplicates_of(source, distancePriority[alphabet[x]][item][1][1])
        if len(repeat) == 2:
            newPair1 = [noListPairs[alphabet[x]][repeat[0]-1], noListPairs[alphabet[x]][repeat[0]]]
            newPair2 = [noListPairs[alphabet[x]][repeat[1]], noListPairs[alphabet[x]][repeat[1] + 1]]
            result1 = [True if newPair1 == list else False for list in distanceCopy[alphabet[x]]]
            indexes1 = 0
            for u in range(len(result1)):
                if result1[u] is True:
                    indexes1 = u
            result2 = [True if newPair2 == list else False for list in distanceCopy[alphabet[x]]]
            indexes2 = 0
            for p in range(len(result2)):
                if result2[p] is True:
                    indexes2 = p
            pairOneDist = distancePriority[alphabet[x]][indexes1][0]
            pairTwoDist = distancePriority[alphabet[x]][indexes2][0]
            if pairOneDist < pairTwoDist:
                del distanceCopy[alphabet[x]][indexes2]
            elif pairTwoDist < pairOneDist:
                del distanceCopy[alphabet[x]][indexes1]
            elif pairTwoDist == pairOneDist:
                varindex1 = indexes1
                varindex2 = indexes2
                if varindex1 < varindex2:
                    del distanceCopy[alphabet[x]][indexes2]
                if varindex2 < varindex1:
                    del distanceCopy[alphabet[x]][indexes1]
noNumDistance = {var: [] for var in string.ascii_lowercase[:qbitnum]}

possiblePairsList = []
for qbit in range(qbitnum):
    for m in range(len(distanceCopy[alphabet[qbit]])):
        result1 = ''.join(i for i in distanceCopy[alphabet[qbit]][m][0] if not i.isdigit())
        result2 = ''.join(i for i in distanceCopy[alphabet[qbit]][m][1] if not i.isdigit())
        noNumDistance[alphabet[qbit]].append([result1, result2])
for qbit in range(qbitnum):
    for m in range(len(noNumDistance[alphabet[qbit]])):
        possiblePairsList.append(noNumDistance[alphabet[qbit]][m])

new_k = []
for elem in possiblePairsList:
    if elem not in new_k:
        new_k.append(elem)
possiblePairsList = new_k
emptyList = []
for thing in range(len(possiblePairsList)):
    possiblePairsList[thing][0], possiblePairsList[thing][1] = possiblePairsList[thing][1], possiblePairsList[thing][0]
    duplicates = list_duplicates_of(possiblePairsList, possiblePairsList[thing])
    xyz = len(duplicates)
    while xyz != 1:
        emptyList.append(possiblePairsList[duplicates[0]])
        xyz -= 1
zzz = [item for item in possiblePairsList if item not in emptyList]
for thing in range(len(emptyList)):
    swapPositions(emptyList[thing], 0, 1)
yyy = [item for item in zzz if item not in emptyList]
for item in range(len(yyy)):
    emptyList.append(yyy[item])
for nm in range(qbitnum):
    for yo in range(len(distanceCopy[alphabet[nm]])):
        Index1 = 0
        Index2 = 0
        for g in range(len(allGatesNum[alphabet[nm]])):
            if allGatesNum[alphabet[nm]][g] == distanceCopy[alphabet[nm]][yo][0]:
                Index1 = g
            if allGatesNum[alphabet[nm]][g] == distanceCopy[alphabet[nm]][yo][1]:
                Index2 = g
        for q in range(len(distanceCopy)):
            for r in range(len(emptyList)):
                if [allGates[alphabet[nm]][Index1], allGates[alphabet[nm]][Index2]] == emptyList[r] and emptyList[r] == ['h', 'h']:
                    allGatesNum[alphabet[nm]][Index1] = "delete"
                    allGatesNum[alphabet[nm]][Index2] = "delete"
                elif [allGates[alphabet[nm]][Index1], allGates[alphabet[nm]][Index2]] == emptyList[r] and emptyList[r] == ['x', 'x']:
                    allGatesNum[alphabet[nm]][Index1] = "delete"
                    allGatesNum[alphabet[nm]][Index2] = "delete"
                else:
                    if [allGates[alphabet[nm]][Index1], allGates[alphabet[nm]][Index2]] == emptyList[r]:
                        allGatesNum[alphabet[nm]][Index1] = f"{emptyList[r][0]} and {emptyList[r][1]}"
                        allGatesNum[alphabet[nm]][Index2] = "delete"
                    elif [allGates[alphabet[nm]][Index2], allGates[alphabet[nm]][Index1]] == emptyList[r]:
                        allGatesNum[alphabet[nm]][Index1] = f"{emptyList[r][0]} and {emptyList[r][1]}"
                        allGatesNum[alphabet[nm]][Index2] = "delete"


for b in range(qbitnum):
    for g in reversed(range(len(allGatesNum[alphabet[b]]))):
        if allGatesNum[alphabet[b]][g] == "delete":
            del allGatesNum[alphabet[b]][g]
for nm in range(qbitnum):
    for g in range(len(allGatesNum[alphabet[nm]])):
        if 'control' not in allGatesNum[alphabet[nm]][g]:
            if 'target' not in allGatesNum[alphabet[nm]][g]:
                oneQubitGates += 1
        if 'control' in allGatesNum[alphabet[nm]][g]:
            twoQubitGates += 1
        if 'target' in allGatesNum[alphabet[nm]][g]:
            twoQubitGates += 1

for gh in range(qbitnum):
    lenBefore = len(singleGates[alphabet[gh]]) + lenBefore
lenBefore = lenBefore + math.ceil(twoQubitGates/2)
lenAfter = math.ceil(twoQubitGates/2) + oneQubitGates

print("Before", lenBefore, ", after", lenAfter)
print("Before ", beforeGates)
print("After ", allGatesNum)