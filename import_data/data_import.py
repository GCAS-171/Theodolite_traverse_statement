"""
Модуль для импорта данных из Google Sheets.

Функции:
- import_data_from_google_sheets(url): Импортирует данные из указанной таблицы Google Sheets и возвращает их в формате pandas DataFrame.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

import logging
logger = logging.getLogger(__name__)

def import_data_from_google_sheets(url: str) -> pd.DataFrame:
    """
    Импортирует данные из Google Sheets.

    :param url: URL таблицы Google Sheets.
    :return: pandas DataFrame с данными.
    """
    # Заглушка: возвращаем пустой DataFrame для тестирования.
    return pd.DataFrame()

# ======================================================================================================================



def get_google_sheet_data(spreadsheet_name):
    logging.info(f"Получение данных из Google Sheets {spreadsheet_name}...")
    # Определяем область доступа
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
    ]

    # Чтение учетных данных из файла ключей Service Account
    credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
    gc = gspread.authorize(credentials)

    # Открытие файла Google Sheets
    sheet = gc.open(spreadsheet_name)
    worksheets = sheet.worksheets()

    data_frames = {}
    ugly_v_grad = []
    direct = []
    prol = []

    x_nach = []
    x_kon = []
    y_nach = []
    y_kon = []

    for i, worksheet in enumerate(worksheets):
        # Получаем все данные из листа
        records = worksheet.get_all_records()
        # Создаем DataFrame из полученных данных
        df = pd.DataFrame(records)

        if i == 0:  # Проверяем, является ли это первым листом
            # Извлечение второго столбца и преобразование в списки с тремя целыми числами
            for value in df.iloc[:, 1].tolist():  # Предполагаем, что данные во втором столбце
                try:
                    numbers = list(map(int, value.split(',')))  # Преобразуем строки в целые числа
                    if len(numbers) == 3:  # Проверяем, что у нас три числа
                        ugly_v_grad.append(numbers[0] + numbers[1]/60 + numbers[2]/3600)  # Добавляем в составной список
                except ValueError:
                    continue  # Игнорируем ошибки преобразования
            # Извлечение третьего столбца, игнорируя последнее значение
            prol = df.iloc[:, 2].tolist()# Сохраняем третий столбец в список без последнего значения

        elif i == 1:  # Проверяем, является ли это вторым листом
            # Извлечение второго столбца и преобразование в списки с тремя целыми числами
            for value in df.iloc[:, 1].tolist():  # Предполагаем, что данные во втором столбце
                try:
                    numbers = list(map(int, value.split(',')))  # Преобразуем строки в целые числа
                    if len(numbers) == 3:  # Проверяем, что у нас три числа
                        direct.append(numbers)  # Добавляем в составной список
                except ValueError:
                    continue

            # Извлечение третьего столбца из второго листа
            third_column_second_sheet = df.iloc[:, 2].tolist()  # Сохраняем третий столбец во список
            # Разделяем direct на два списка
            mid_index = len(direct) // 2
            direct_n = direct[:mid_index]  # Первый список
            direct_k = direct[mid_index:]  # Второй список
            # Разделяем третий столбец на два разных списка
            mid_index = len(third_column_second_sheet) // 2
            x_nach = third_column_second_sheet[:mid_index]  # Первый список
            x_kon = third_column_second_sheet[mid_index:]  # Второй список
            # Извлечение четвертого столбца из второго листа
            fourth_column_second_sheet = df.iloc[:, 3].tolist()  # Сохраняем четвертый столбец во список
            # Разделяем четвертый столбец на два разных списка
            mid_index_fourth = len(fourth_column_second_sheet) // 2
            y_nach = fourth_column_second_sheet[:mid_index_fourth]  # Первый список
            y_kon = fourth_column_second_sheet[mid_index_fourth:]  # Второй список

        data_frames[worksheet.title] = df

    logging.info(f"... выполнен успешно.")

    return data_frames, ugly_v_grad, direct_n, direct_k, prol, x_nach, x_kon, y_nach, y_kon  # Возвращаем DataFrames и списки


def enother_get_data(spreadsheet_name: str):
    dataframes,  ugly_v_grad, _, __,prol, *lishnie_dannye = get_google_sheet_data(spreadsheet_name)
    dataframes["sheet1"]["Десятичный угол"] = ugly_v_grad
    dataframes["sheet1"]["Проложение в метрах"] = prol
    dataframes["sheet1"].drop(columns=['Измеренные углы', 'Горизонт прол'], inplace=True)

    logging.info(f"Передаваемые данные: {dataframes}")

    point_first = (dataframes["sheet2"].iloc[0, 2], # X первой точки
                   dataframes["sheet2"].iloc[0, 3], # Y первой точки
                   dataframes["sheet2"].iloc[0, 1], # дирекционный угол начальный
                   dataframes["sheet2"].iloc[0, 0], # название (имя) первой точки
                   dataframes["sheet2"].iloc[0, 4]) # название (имя) начальной точки
    point_last  = (dataframes["sheet2"].iloc[1, 2], # X последней точки
                   dataframes["sheet2"].iloc[1, 3], # Y последней точки
                   dataframes["sheet2"].iloc[1, 1], # дирекционный угол конечный
                   dataframes["sheet2"].iloc[1, 0], # название (имя) последней точки
                   dataframes["sheet2"].iloc[1, 4]) # название (имя) конечной точки

    # logging.info(point_first, point_last)
    return dataframes["sheet1"], point_first, point_last

if __name__ == '__main__':
    spreadsheet_name = 'project'  # Замените на название вашей таблицы
    ddd = enother_get_data(spreadsheet_name)
    data, ugly_v_grad, direct_n, direct_k, prol, x_nach, x_kon, y_nach, y_kon = get_google_sheet_data(spreadsheet_name)

    # Выводим данные из каждого листа
    for title, df in data.items():
        print(f"Данные из листа: {title}")
        print(df)
        print("\n")  # Пустая строка для разделения данных разных листов


    print(f"{ddd=}")