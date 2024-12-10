"""
Модуль для предварительной обработки данных.

Функции:
- preprocess_data(df): Выполняет предварительную обработку данных.
"""
import sys

import numpy
import pandas as pd
import numpy as np
from icecream import ic

import logging
logger = logging.getLogger(__name__)

def correct_angle(A):
    if A < 0:
        return A + 360.
    if A > 360:
        return A - 360.
    return A
def preprocess_data(dataframes: pd.DataFrame, point_first, point_last) -> pd.DataFrame:
    """
    Выполняет предварительную обработку данных.

    :param df: pandas DataFrame с данными.
    :return: Обработанный pandas DataFrame.
    """
    # Заглушка: возвращаем тот же DataFrame без изменений.

    logger.info('Выполняется предварительная обработка данных.')

    # logger.info('Точки: ',point_first[2], point_last[2])

    bт = point_first[2] - point_last[2] + 180 * dataframes['Десятичный угол'].count()
    bпр = dataframes['Десятичный угол'].sum()
    fb=(bпр-bт)
    fbдоп=round((dataframes['Десятичный угол'].count()**0.5),1)
    Svb=-1*fb
    vb=Svb/dataframes['Проложение в метрах'].sum()
    Sd=dataframes['Проложение в метрах'].sum()
    ic(bт,bпр,fb,fbдоп,Svb,vb,Sd)

    dataframes['Исправленные углы'] = dataframes['Десятичный угол'].add(vb)
    dataframes['Исправленные углы'] = dataframes['Исправленные углы']

    # ic(dataframes['Исправленные углы'])

    dataframes['Дир. углы'] = numpy.zeros(dataframes['Исправленные углы'].count())
    dataframes.loc[0, 'Дир. углы'] = point_first[2]

    for i in range(1, dataframes['Исправленные углы'].count()):
        dataframes.loc[i,'Дир. углы'] = correct_angle( dataframes.loc[i-1, 'Дир. углы'] + 180 - dataframes.loc[i-1, 'Исправленные углы'] )

    Last_angle = correct_angle( dataframes.loc[dataframes['Исправленные углы'].count()-1, 'Дир. углы'] + 180 -
                                dataframes.loc[dataframes['Исправленные углы'].count()-1, 'Исправленные углы'] )
    ic(dataframes)
    ic(Last_angle)

    return dataframes #, Подвал и последний угол









    return dataframes