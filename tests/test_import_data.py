import pytest
from import_data.data_import import import_data_from_google_sheets

def test_import_data_from_google_sheets():
    """Тестируем импорт данных из Google Sheets."""
    
    url = "https://example.com/sheet"  # Пример URL таблицы Google Sheets
    
    # Проверяем, что функция возвращает DataFrame
    df = import_data_from_google_sheets(url)
    
    assert isinstance(df, pd.DataFrame), "Данные должны быть в формате DataFrame"