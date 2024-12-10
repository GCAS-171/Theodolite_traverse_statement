"""
Модуль для выполнения вычислений.

Функции:
- perform_calculations(df): Выполняет необходимые вычисления над данными.
"""
import numpy
import pandas as pd
import numpy as np
from icecream import ic

import logging
logger = logging.getLogger(__name__)

def perform_calculations(df: pd.DataFrame, point_first, point_last):
    """
    Выполняет необходимые вычисления над данными.

    :param df: pandas DataFrame с данными.
    :return: Словарь с результатами вычислений.
    """
    # Заглушка: возвращаем пустой словарь для тестирования.
    logger.info('Выполняются необходимые вычисления над данными.')
    df['Дельта x'] = np.zeros(df['Дир. углы'].count())
    df['Дельта y'] = np.zeros(df['Дир. углы'].count())

    df['Дир. рад'] = df['Дир. углы'] * np.pi / 180

    df['Дельта х'] = df['Проложение в метрах'] * np.cos(df['Дир. рад'])
    df['Дельта y'] = df['Проложение в метрах'] * np.sin(df['Дир. рад'])

    sdx= df['Дельта х'].sum() #сумма дельта практ х
    sdy = df['Дельта y'].sum()
    sxt = point_last[0] - point_first[0] #
    syt = point_last[1] - point_first[1]
    fx= sdx-sxt
    fy =sdy-syt
    fabc=np.sqrt(fx**2+fy**2)
    Sd = df['Проложение в метрах'].sum()
    fo=1/(Sd/fabc)
    v=-fx/4  # считаем поправкудля прирощ

    df['Дельта х исп'] = df['Проложение в метрах'] * np.cos(df['Дир. рад'])+v #исправленные 9 столб
    df['Дельта y исп'] = df['Проложение в метрах'] * np.sin(df['Дир. рад'])+v #исправленные 10 столб

    df['X'] = np.zeros(df['Дир. углы'].count())
    df.loc[0, 'X'] = point_first[0]
    df['Y'] = np.zeros(df['Дир. углы'].count())
    df.loc[0, 'Y'] = point_first[1]

    for i in range(1, df['Дельта х исп'].count()):
        df.loc[i,'X'] = ( df.loc[i-1, 'X'] +  df.loc[i, 'Дельта х исп'] )

    for i in range(1, df['Дельта y исп'].count()):
        df.loc[i,'Y'] = ( df.loc[i-1, 'Y'] +  df.loc[i, 'Дельта y исп'] )

    ic(df['Дельта х'],df['Дельта y'],df['Дельта х исп'] ,df['Дельта y исп'], df['X'], df['Y'])
    ic(sdx,sdy, sxt, syt , fx, fy, fabc, Sd, fo)

    return {}