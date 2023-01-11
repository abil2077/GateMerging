import string
alphabet = list(string.ascii_lowercase)
file = input("file name: ")
f1 = open(file, 'r')
f2 = open(f'{file}copy', 'w')
for line in f1:
    if "q_" in line:
        start_index = line.index("q_")
        end_index = line.index("[")
        if end_index < start_index:
            end_index = line.index("[", end_index + 1)
        tmp = line.replace(line[start_index: end_index], alphabet[int(line[start_index + 2: end_index])])
        try:
            start_index = line.index("q_", start_index + 1)
            end_index = line.index("[", end_index + 1)
            tmp = tmp.replace(line[start_index: end_index], alphabet[int(line[start_index + 2: end_index])])
        except:
            print("")
        f2.write(tmp)
    if "q_" not in line:
        f2.write(line)
f1.close()
f2.close()
