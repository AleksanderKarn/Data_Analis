import csv
import os

list_dict = []    ### список словарей создаваемый и ззначений файла функциеу list_dict_creator
count = 0            ### счетчик файлов на которые разбит изначальный файл ###
result = []          ### список с результатом сортировки записываемыъ в файл
list_for_sort = []      ### временный список полученных значений в зависимости от тикеров отправляющийся в сортировку
list_after_sort = []            ### список накопитель данных из list_for_sort в который добавляются данные после сортировки
cache = []             ## кэш


def partition(list_dict, low, high):
    """Функция для нахождения среднего
    значения  из урока по алгоритмам сортировки квик-сорт"""
    pivot = list_dict[(low + high) // 2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while list_dict[i] < pivot:
            i += 1
        j -= 1
        while list_dict[j] > pivot:
            j -= 1
        if i >= j:
            return j
        list_dict[i], list_dict[j] = list_dict[j], list_dict[i]


def quick_sort(list_dict):
    ''' функция сортировщик'''
    def _quick_sort(items, low, high):
        if low < high:
            split_index = partition(items, low, high)
            _quick_sort(items, low, split_index)
            _quick_sort(items, split_index + 1, high)

    _quick_sort(list_dict, 0, len(list_dict) - 1)


def get_data(sort_columns, limit):
    """функция вызывает функцию создающую список словарей """
    dict_creator()
    global list_for_sort, list_after_sort, s_, count

    list_for_sort.clear()
    ## разделяет типы данных float и int
    for i in range(len(list_dict)):
        if list_dict[i][sort_columns] != '':
            if sort_columns != 'volume':
                list_for_sort.append(float(list_dict[i][sort_columns]))
            else:
                list_for_sort.append(int(list_dict[i][sort_columns]))

    quick_sort(list_for_sort)
    list_after_sort += list_for_sort[:limit] ## добавить отсортированные данные в другой список
    ## если еще есть файлы не отсортированные то сортируем пока они не закончатся
    if os.path.exists('all_stocks_5yr_part_' + str(count - 1) + '.csv'):
        get_data(sort_columns, limit)
    else:
        ## отсортировать между собой отсортированные кусочки из всех файлов
        quick_sort(list_after_sort)
        list_after_sort = list_after_sort[:limit]    ## изза того что значения могут повторяться их в списке может оказатся больше чем указано в limit поэтому после сортировки мы еще раз берем срез по нужной нам длине
        list_after_sort = list(map(str, list_after_sort)) ## привожу элементы результирующего списка к строке для того чтобы можно было сравнивать их с соответствующими элементами словарей
        count = 0
        ## прохожу циклом по отсортированным элементам списка
        for i in list_after_sort:
            ## вложенный цикл для сравнения элементов из отсортированного получившегося списка со всеми элементами файла
            for j in range(len(list_dict)):
                ## метод вытаскивающий из общего обьема данных те у которых совпадают элементы словаря заданные в сортировке
                if i == list_dict[j][sort_columns]:
                    count += 1
                    result.append(list_dict[j])
    return result


def dict_creator():
    """Функцияф создает коллекцию значений
    из списка в формате списка словарей"""
    global count
    count += 1
    list_dict.clear()  ## очищаем отработанные данные - ЭКОНОМИМ ОПЕРАТИВКУ

    if os.path.exists('all_stocks_5yr_part_' + str(count) + '.csv'):
        with open('all_stocks_5yr_part_' + str(count) + '.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                list_dict.append(row)


def select_sorted(get_data, sort_columns="high", limit=10, order='desc'):
    """функция для получения выборки значений по заданным араметрам из предоставленного файла csv """
    global result, d, cache

    ## генерирую уникальное имя файла на основе входных данных дял поиска
    filename = (f'{sort_columns}_{limit}_{order}.csv')
    filename = filename.replace('-', '')
    ## проверка на существоввание файла (кэша)
    if os.path.exists(f'data/{filename}'):
        print('Результат взят Из кэша: ')
        ## открыть готовый файл с результатом по данному запросу
        with open(os.path.join('./data', filename), 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cache.append(row)
            print(f'Результат: {cache}')
            return cache
    else:
        print('Осуществляется поиск всех результатов....')
        ## сортируем файл частями
        get_data(sort_columns, limit)
        ## развернуть список если указана сортировка по убыванию
        if order != 'asc':
            result = result[::-1]
        with open(os.path.join('./data', filename), 'w', newline='') as fs:
            w = csv.DictWriter(fs, fieldnames=result[0].keys(), delimiter=',')
            w.writeheader()
            for i in result[:limit]:
                w.writerow(i)
            print(f'Результат записан в файл: {filename}')
            print(f'Результат: {result[:limit]}')


def run_():
    if not os.path.isdir('data'):
        os.mkdir('data')

    sort_to_price = [1, 'open', 'close', 'high', 'low', 'volume']
    sort_columns = input(f'Сортировать по цене:\nopen   (1)\nclose  (2)\nhigh   [3]\nlow    (4)\nvolume (5)')
    if sort_columns == '':
        sort_columns = '3'
    sort_columns = sort_to_price[int(sort_columns)]

    asc_desc = [1, 'desc', 'asc']
    order = input(f'Порядок по убыванию [1] / возрастанию (2): ')
    if order == '':
        order = '1'
    order = asc_desc[int(order)]

    limit = input(f'Ограничение выборки [10]: ')
    if limit == '':
        limit = '10'
    select_sorted(get_data, sort_columns=sort_columns, limit=int(limit), order=order)

if __name__ == '__main__':
    run_()