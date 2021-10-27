import numpy as np

with open('Poil_contig.fa') as contig:
    contig = contig.readlines()
    l = []

    for line in contig:
        if line.startswith('>'):
            l.append(float(line.split('_')[1][3:]))

print('общее кол-во контигов:', len(l))
print('общая длина контигов:', np.sum(l))
print('длина самого длинного контига:', np.max(l))

s = np.sum(l)/2
l.sort()
c = 0
for i in l[-1::-1]:
    c += i
    if c >= s:
        print('N50:', i)
        break

with open('Poil_scaffold.fa') as scaffold:
    scaffold = scaffold.readlines()
    l = []

    for line in scaffold:
        if line.startswith('>'):
            l.append(float(line.split('_')[1][3:]))
            if float(line.split('_')[1][3:]) == 3831286.0:
                print(line)


print('общее кол-во скаффолдов:', len(l))
print('общая длина скаффолдов:', np.sum(l))
print('длина самого длинного скаффолда:', np.max(l))

s = np.sum(l)/2
l.sort()
c = 0
for i in l[-1::-1]:
    c += i
    if c >= s:
        print('N50:', i)
        break

with open('Poil_gapClosed.fa') as scaffold:
    scaffold = scaffold.readlines()
    l = []

    for line in scaffold:
        if line.startswith('>'):
            l.append(float(line.split('_')[1][3:]))
            if float(line.split('_')[1][3:]) == 2385.0:
                print(line)


print('общее кол-во скаффолдов:', len(l))
print('общая длина скаффолдов:', np.sum(l))
print('длина самого длинного скаффолда:', np.max(l))

with open('max_scaffold.fa') as max_scaf:
    max_scaf = max_scaf.read()
    c = 0
    for i in range(len(max_scaf)-1):
        if max_scaf[i] == 'N' and max_scaf[i] != max_scaf[i+1]:
            c += 1
    print('Общая длина гэпов:', max_scaf.count('N'))
print('Количество гэпов:', c)

with open('max_scaffold_gapClosed.fa') as max_scaf:
    max_scaf = max_scaf.read()
    c = 0
    for i in range(len(max_scaf)-1):
        if max_scaf[i] == 'N' and max_scaf[i] != max_scaf[i + 1]:
            c += 1
    print('Общая длина гэпов:', max_scaf.count('N'))
print('Количество гэпов:', c)