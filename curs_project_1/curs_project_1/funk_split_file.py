
def funk_split(chunk_size=10 ** 5):
    '''функция разделяет большие файлы
     на файлы с chunk_size колличеством строк'''
    ##chunk_size = 100к строк изменяемый параметр зависит от мощности сервера(от колличества оперативной памяти)

    def write_chunk(part, lines):
        '''функция получает в параметрах счетчик файлов
        и  список из 100к строк из прочитанног офайла '''
        ## создаю файлы по 100к строк в каждом
        with open('all_stocks_5yr_part_' + str(part) + '.csv', 'w') as f_out:
            f_out.write(header)
            f_out.writelines(lines)

    ## читаю файл и сохраняю указанное колличество строк в список lines
    with open('all_stocks_5yr.csv', 'r') as f:
        count = 0
        header = f.readline()
        lines = []

        for line in f:
            count += 1
            lines.append(line)
            ## eсли счетчик строк делится на заданное значения фильтра без остатка то пора вести запись в новый файл
            if count % chunk_size == 0:

                write_chunk(count // chunk_size, lines)
                lines = []

        if len(lines) > 0:
            write_chunk((count // chunk_size) + 1, lines)


if __name__ == '__main__':
    funk_split()
