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

    platanus scaffold -o Poil -t 1 -c Poil_contig.fa -IP1 oil_R1_seq.fastq.trimmed oil_R2_seq.fastq.trimmed -OP2 oilMP_S4_L001_R1_001_seq.fastq.int_trimmed oilMP_S4_L001_R2_001_seq.fastq.int_trimmed 2> scaffold.log

-> удаление гэпов с **platanus gap_close**:

    platanus gap_close -o Poil_gap_close -t 1 -c Poil_scaffold.fa -IP1 oil_R1_seq.fastq.trimmed oil_R2_seq.fastq.trimmed -OP2 oilMP_S4_L001_R1_001_seq.fastq.int_trimmed oilMP_S4_L001_R2_001_seq.fastq.int_trimmed 2> gapclose.log

-> удаление лишних файлов осуществляется командой **rm**

-> копирование файлов с удаленной машины на локальную осуществляется с помощью команды **scp**

# Сравнение качества чтений до и после подрезания:

->

->

-> Выводы:

1.
2.

# Код python:

-> Анализ полученных контигов (общее кол-во контигов, их общая длина, длина самого длинного контига, N50)

-> Анализ полученных скаффолдов (общее кол-во скаффолдов, их общая длина, длина самого длинного скаффолда, N50)

-> Найти самый длинный скаффолд, посчитать количество гэпов и общую длину:
