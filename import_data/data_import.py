"""
Модуль для импорта данных из Google Sheets.

Функции:
- import_data_from_google_sheets(url): Импортирует данные из указанной таблицы Google Sheets и возвращает их в формате pandas DataFrame.
"""

import pandas as pd

def import_data_from_google_sheets(url: str) -> pd.DataFrame:
    """
    Импортирует данные из Google Sheets.

    :param url: URL таблицы Google Sheets.
    :return: pandas DataFrame с данными.
    """
    # Заглушка: возвращаем пустой DataFrame для тестирования.
    return pd.DataFrame()

# ======================================================================================================================

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def get_google_sheet_data(spreadsheet_name):
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
    ugly_v_grad = []  # Список для хранения данных из второго столбца первого листа
    nested_list_2 = []  # Список для хранения данных из второго столбца второго листа
    third_column_first_sheet = []  # Список для хранения данных из третьего столбца первого листа
    # Список для хранения данных из второго столбца второго листа
    third_column_list_a = []  # Список для хранения первой половины третьего столбца второго листа
    third_column_list_b = []  # Список для хранения второй половины третьего столбца второго листа
    fourth_column_list_a = []
    fourth_column_list_b = []  # Список для второй половины четвертого столбца второго листа

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
                        ugly_v_grad.append(numbers)  # Добавляем в составной список
                except ValueError:
                    continue  # Игнорируем ошибки преобразования
            # Извлечение третьего столбца, игнорируя последнее значение
            third_column_first_sheet = df.iloc[:, 2].tolist()[:-1]  # Сохраняем третий столбец в список без последнего значения

        elif i == 1:  # Проверяем, является ли это вторым листом
            # Извлечение второго столбца и преобразование в списки с тремя целыми числами
            for value in df.iloc[:, 1].tolist():  # Предполагаем, что данные во втором столбце
                try:
                    numbers = list(map(int, value.split(',')))  # Преобразуем строки в целые числа
                    if len(numbers) == 3:  # Проверяем, что у нас три числа
                        nested_list_2.append(numbers)  # Добавляем в составной список
                except ValueError:
                    continue

            # Извлечение третьего столбца из второго листа
            third_column_second_sheet = df.iloc[:, 2].tolist()  # Сохраняем третий столбец во список
            # Разделяем nested_list_2 на два списка
            mid_index = len(nested_list_2) // 2
            nested_list_2a = nested_list_2[:mid_index]  # Первый список
            nested_list_2b = nested_list_2[mid_index:]  # Второй список
            # Разделяем третий столбец на два разных списка
            mid_index = len(third_column_second_sheet) // 2
            third_column_list_a = third_column_second_sheet[:mid_index]  # Первый список
            third_column_list_b = third_column_second_sheet[mid_index:]  # Второй список
            # Извлечение четвертого столбца из второго листа
            fourth_column_second_sheet = df.iloc[:, 3].tolist()  # Сохраняем четвертый столбец во список
            # Разделяем четвертый столбец на два разных списка
            mid_index_fourth = len(fourth_column_second_sheet) // 2
            fourth_column_list_a = fourth_column_second_sheet[:mid_index_fourth]  # Первый список
            fourth_column_list_b = fourth_column_second_sheet[mid_index_fourth:]  # Второй список

        data_frames[worksheet.title] = df

    return data_frames, ugly_v_grad, nested_list_2a, nested_list_2b, third_column_first_sheet, third_column_list_a, third_column_list_b, fourth_column_list_a, fourth_column_list_b  # Возвращаем DataFrames и списки

if __name__ == '__main__':
    spreadsheet_name = 'project'  # Замените на название вашей таблицы
    data, ugly_v_grad, nested_list_2a, nested_list_2b, third_column_values, third_column_list_a, third_column_list_b, fourth_column_list_a, fourth_column_list_b = get_google_sheet_data(spreadsheet_name)

    # Выводим данные из каждого листа
    for title, df in data.items():
        print(f"Данные из листа: {title}")
        print(df)
        print("\n")  # Пустая строка для разделения данных разных листов

    # Выводим вложенные списки из второго столбца первого и второго листов
    print("Измеренные углы:")
    print(ugly_v_grad, "\n")
    print("Дирекционный углол (начальный):")
    print(nested_list_2a)
    print("Дирекционный углол (конечный):")
    print(nested_list_2b, "\n")
    print("Горизонтальные проложения:")
    print(third_column_values, "\n")
    print("Координаты X исходных точек:")
    print("X первой точки:")
    print(third_column_list_a)
    print("X конечной точки:")
    print(third_column_list_b, "\n")
    print("Координаты Y исходных точек:")
    print("Y первой точки:")
    print(fourth_column_list_a)
    print("Y конечной точки:")
    print(fourth_column_list_b)