
import os
import glob


dir_name = 'performance50'

counts = []
for i in range(1000):
    directory = os.path.join('modelss', dir_name, 'antimony', 'performance50_' + str(i) + '.txt')
    print(directory)
    with open(directory) as filee:
        count = 0
        lines = filee.readlines()
        for line in lines:
            if line[0] == 'J':
                count += 1
        counts.append(count)


print(sum(counts)/len(counts))

quit()
files = glob.glob(os.path.join(directory, '*'))

counts = []
for file in files:
    count = 0
    # print(file)
    readfile = open(file, 'r')
    lines = readfile.readlines()
    for line in lines:
        if line[0] == 'J':
            count += 1
    counts.append(count)

# for each in counts:
#     print(each)
print()
print(sum(counts)/len(counts))
