import logging
from .\import_data\import_data import enother_get_data
#from .\preprocessing\preprocessing import preprocessing
#from .\computation\computation import computation
from .\reporting\webreport import html_report
from .\reporting\pdfreport import pdf_report


# Настройка логирования 
logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Запуск программы...")

    google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_

    dataframes = enother_get_data(google_sheet_url)
    datapreprocessing = preprocessing(dataframes)
    result = computation(datapreprocessing)
    html_doc = html_report(result)
    pdf_doc = pdf_report(result)

    
if __name__ == "__main__":
    main()