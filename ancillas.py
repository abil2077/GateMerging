import string
alphabet = list(string.ascii_lowercase)
file = input("file name: ")
f1 = open(f'{file}copy', 'r')
f2 = open(f'{file}copycopy', 'w')
data = {}
ancillaNum = 0
letterBefore = None
with open(f'{file}copy', "r") as file_in:
    allLines = file_in.readlines()
for line in allLines:
    if 'qreg ancilla' in line:
        ancillaNum += 1
for Line in range(len(allLines)):
    if "qreg ancilla0" in allLines[Line]:
        letterBefore = allLines[Line - 1][5]
for t in range(ancillaNum):
    data[f"ancilla{t}"] = alphabet[alphabet.index(letterBefore) + 1 + t]
for line in f1:
    if "ancilla" in line:
        start_index = line.index("ancilla")
        end_index = line.index("[")
        if end_index < start_index:
            end_index = line.index("[", end_index + 1)
        tmp = line.replace(line[start_index: end_index], data[line[start_index: end_index]])
        try:
            start_index = line.index("ancilla", start_index + 1)
            end_index = line.index("[", end_index + 1)
            tmp = tmp.replace(line[start_index: end_index], data[line[start_index: end_index]])
        except:
            print("")
        f2.write(tmp)
    if "ancilla" not in line:
        f2.write(line)
f1.close()
f2.close()