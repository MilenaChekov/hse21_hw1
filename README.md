hse21_hw1

# Список всех используемых команд:


-> ssh для входа на сервера

-> создание ссылки: **ln -s /путь к файлу**

-> выбрать случайные чтения:

    seqtk sample -s119 oil_R1.fastq 5000000 > oil_R1_seq.fastq
    seqtk sample -s119 oil_R2.fastq 5000000 > oil_R2_seq.fastq
    seqtk sample -s119 oilMP_S4_L001_R1_001.fastq 1500000 > oilMP_S4_L001_R1_001_seq.fastq
    seqtk sample -s119 oilMP_S4_L001_R2_001.fastq 1500000 > oilMP_S4_L001_R2_001_seq.fastq

-> запустить **fastqc и multiqc** для оценки качества сырых данных:

    fastqc -o fastQc *seq.fastq
    mkdir fastQc
    cd fastQc
    multiqc .

-> улучшение качества данных с помощью **platanus_trim/platanus_internal_trim**:

    platanus_trim oil_R1_seq.fastq oil_R2_seq.fastq
    platanus_internal_trim oilMP_S4_L001_R1_001.fastq oilMP_S4_L001_R2_001.fastq

-> запустить **fastqc и multiqc** для оценки качества подрезанных чтений:

    fastqc -o fastQc_trimmed *fastq.trimmed
    fastqc -o fastQc_trimmed *fastq.int_trimmed
    mkdir fastQc_trimmed
    cd fastQc_trimmed
    multiqc .

-> сборка контигов с помощью **platanus assemble**:

    platanus assemble -o Poil -t 1 -m 28 -f oil_R1_seq.fastq.trimmed oil_R2_seq.fastq.trimmed 2> assemble.log

-> сборка скаффолдов с использованием **platanus scaffold**:

    platanus scaffold -o Poil -t 1 -c Poil_contig.fa -IP1 oil_R1_seq.fastq.trimmed oil_R2_seq.fastq.trimmed -OP2 oilMP_S4_L001_R1_001_seq.fastq.int_trimmed     oilMP_S4_L001_R2_001_seq.fastq.int_trimmed 2> scaffold.log

-> поиск самого длинного скаффолда (самые длинные скаффолды находим в питоне):

    echo scaffold1_len3831286_cov232 > max_scaffold.txt
    seqtk subseq Poil_scaffold.fa max_scaffold.txt > max_scaffold.fa
    
-> удаление гэпов с **platanus gap_close**:

    platanus gap_close -o Poil -t 1 -c Poil_scaffold.fa -IP1 oil_R1_seq.fastq.trimmed oil_R2_seq.fastq.trimmed -OP2 oilMP_S4_L001_R1_001_seq.fastq.int_trimmed oilMP_S4_L001_R2_001_seq.fastq.int_trimmed 2> gapclose.log

-> поиск самого длинного скаффолда:

    echo scaffold62_cov2385 > max_scaffold.txt
    seqtk subseq Poil_gapClosed.fa max_scaffold.txt > max_scaffold_gapClosed.fa

-> удаление лишних файлов осуществляется командой **rm**

-> копирование файлов с удаленной машины на локальную осуществляется с помощью команды **scp**

# Сравнение качества чтений до и после подрезания:

-> Сырые данные
<img width="1093" alt="Снимок экрана 2021-10-27 в 21 53 48" src="https://user-images.githubusercontent.com/60537367/139128858-1c860cd3-eb96-4b70-9eaa-246195844bd0.png">

<img width="1092" alt="Снимок экрана 2021-10-27 в 21 50 58" src="https://user-images.githubusercontent.com/60537367/139128444-bae7865f-1aff-4883-b1a4-c5228ed20c14.png">

<img width="1094" alt="Снимок экрана 2021-10-27 в 21 55 21" src="https://user-images.githubusercontent.com/60537367/139129060-f776a449-65a7-49c3-876a-b5cbdca74341.png">

-> После обработки
<img width="1098" alt="Снимок экрана 2021-10-27 в 21 54 02" src="https://user-images.githubusercontent.com/60537367/139128886-a3f30c03-570e-437d-a470-a671e3efc0cd.png">

<img width="1092" alt="Снимок экрана 2021-10-27 в 21 51 24" src="https://user-images.githubusercontent.com/60537367/139128507-17cc5571-db6d-48c7-a179-2bd1f806b146.png">

<img width="1093" alt="Снимок экрана 2021-10-27 в 21 55 08" src="https://user-images.githubusercontent.com/60537367/139129039-66c55871-1744-440e-918d-705e78bef895.png">

-> Выводы (их также можно проследить на скриншотах ниже - сверху до, ниже после):

1. Качество улучшилось 
2. Длина уменьшилась
3. Удалились адаптеры
<img width="1088" alt="Снимок экрана 2021-10-27 в 21 56 54" src="https://user-images.githubusercontent.com/60537367/139129272-b4148078-c61b-405a-b116-0734b6bcbfbb.png">
<img width="1089" alt="Снимок экрана 2021-10-27 в 21 57 13" src="https://user-images.githubusercontent.com/60537367/139129315-39210950-e6dd-4adb-a50e-a8ff288a8fea.png">

# Код python:

-> Анализ полученных контигов (общее кол-во контигов, их общая длина, длина самого длинного контига, N50):
    
    with open('Poil_contig.fa') as contig:
        contig = contig.readlines()

        for line in contig:
            l = []
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

-> Анализ полученных скаффолдов с гэпами(общее кол-во скаффолдов, их общая длина, длина самого длинного скаффолда, N50):

    with open('Poil_scaffold.fa') as scaffold:
        scaffold = scaffold.readlines()

        for line in scaffold:
            l = []
            if line.startswith('>'):
                l.append()
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

-> Найти самый длинный скаффолд, посчитать количество гэпов и общую длину:

    with open('max_scaffold.fa') as max_scaf:
        max_scaf = max_scaf.read()
        c = 0
        for i in range(len(max_scaf)-1):
            if max_scaf[i] == 'N' and max_scaf[i] != max_scaf[i+1]:
                c += 1
        print('Общая длина гэпов:', max_scaf.count('N'))
    
    print('Количество гэпов:', c)
 
-> Анализ полученных скаффолдов с удалением гэпов (общее кол-во скаффолдов, их общая длина, длина самого длинного скаффолда, N50):

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

    s = np.sum(l)/2
    l.sort()
    c = 0
    for i in l[-1::-1]:
        c += i
        if c >= s:
            print('N50:', i)
            break

-> Найти самый длинный скаффолд, посчитать количество гэпов и общую длину:
    
    with open('max_scaffold_gapClosed.fa') as max_scaf:
        max_scaf = max_scaf.read()
        c = 0
        for i in range(len(max_scaf)-1):
            if max_scaf[i] == 'N' and max_scaf[i] != max_scaf[i + 1]:
                c += 1
        print('Общая длина гэпов:', max_scaf.count('N'))
    print('Количество гэпов:', c)

<img width="214" alt="Снимок экрана 2021-10-27 в 23 25 12" src="https://user-images.githubusercontent.com/60537367/139141602-a8f3188a-d86a-4cf5-99b7-fc26c0adc65d.png">
все гэпы удалены
