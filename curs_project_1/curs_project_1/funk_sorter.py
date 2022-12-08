import csv
import os

list_dict = []  ### список словарей создаваемый и ззначений файла функциеу list_dict_creator
count = 0  ### счетчик файлов на которые разбит изначальный файл ###
result = []  ### список для сохранения результатов работы функции поиска значения sorter


def sorter(name, date):
    """Функция осуществляет выбор
    фильтра для запуска процесса поиска
     значения в прочитанных кусочках файлов
      которые были сохранены во временную
      переменную list_dict """
    global result
    ## генерация данных в list_dict
    list_dict_creator()

    ## проверка условий
    if name != 'all' and date != 'all':
        for i in list_dict:
            if i['date'] == date and i['Name'] == name:
                result.append(i)
        ## проверка существования файлов для понимания закончили мы с поиском значения или продолжить
        if os.path.exists('all_stocks_5yr_part_' + str(count) + '.csv'):
            sorter(name, date)

    elif name == 'all':
        for i in list_dict:
            if i['date'] == date:
                result.append(i)
        if os.path.exists('all_stocks_5yr_part_' + str(count) + '.csv'):
            sorter(name, date)

    else:
        for i in list_dict:
            if i['Name'] == name:
                result.append(i)
        if os.path.exists('all_stocks_5yr_part_' + str(count) + '.csv'):
            sorter(name, date)
    return result


def list_dict_creator():
    """Функцияф создает коллекцию значений
    из списка в формате списка словарей"""
    global count
    count += 1  ## изменение счетчика для корректного открытия следующего файла
    list_dict.clear()  ## очистка переработанной информации

    ## если файл существует
    if os.path.exists('all_stocks_5yr_part_' + str(count) + '.csv'):
        with open('all_stocks_5yr_part_' + str(count) + '.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                list_dict.append(row)


def data_name_sorted(f, name='all', date='all'):
    """Функция сортировки и записи в файл данных
    из файла по заданным параметрам date и name"""
    global result
    ## генерирую уникальное имя файла на основе входных данных дял поиска
    filename = (f'{name}_{date}.csv')
    filename = filename.replace('-', '')
    ## проверка уникальности запроса пользователя
    if os.path.exists(f'data/{filename}'):
        print('Результат взят Из кэша: ')
        ## открыть файл для чтения
        with open(os.path.join('./data', filename), 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                list_dict.append(row)
            print(f'Результат: {list_dict}')
            return list_dict
    else:
        ## если входные параметры уникальны и в кэше нет занчения то осуществляется поиск по разбитому файлу
        print('Осуществляется поиск всех результатов....')
        f(name, date)
        ## если список с результатом пуст
        if result == []:
            print('Значений не найдено')
        else:
            ## создал файл для записи
            with open(os.path.join('./data', filename), 'w', newline='') as fs:
                w = csv.DictWriter(fs, fieldnames=result[0].keys(), delimiter=',')
                w.writeheader()
                for i in result:
                    w.writerow(i)
                    print(f'Результат записан в файл: {filename}')



def run_():
    if not os.path.isdir('data'):
        os.mkdir('data')
    date = input(f'Дата в формате yyyy-mm-dd [all]: ')
    if date == '':
        date = 'all'
    name = input(f'Тикер [all]: ').upper()
    if name == '':
        name = 'all'
    data_name_sorted(sorter, name=name, date=str(date))


if __name__ == '__main__':
    run_()
