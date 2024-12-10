import logging
from import_data.data_import import enother_get_data
from preprocessing.preprocessing import preprocess_data
from computation.calculations import perform_calculations
from reporting.web_report import generate_web_report
from reporting.pdf_report import generate_pdf_report


import logging
logger = logging.getLogger(__name__)


# Настройка логирования 
logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Запуск программы...")

    # google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT3_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_4_
    google_sheet_name = "project"

    dataframe, point_first, point_last = enother_get_data(google_sheet_name)

    # dataframe["Градусы"] = dataframe["Измеренные углы"]
    #
    # df["угол"] = df["градусы"] + df["минуты"] / 60 + df["секунды"] / 3600

    logging.info(dataframe.info())
    datapreprocessing = preprocess_data(dataframe, point_first, point_last)
    result = perform_calculations(dataframe, point_first, point_last)
    html_doc = generate_web_report(result)
    pdf_doc = generate_pdf_report(result)

    
if __name__ == "__main__":
    main()
    #внести в изначальную таблицу значения о приборе