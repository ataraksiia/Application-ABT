from src.reports import spending_by_category
from src.services import main_function_services
from src.views import home_page

if __name__ == "__main__":
    print(home_page("2020-12-12 05:59:59"))
    main_function_services(
        "../data/operations.xls",
        "2021",
        "09",
        [
            {"Дата операции": "29.09.2021", "Сумма операции": -4429.0},
            {"Дата операции": "29.09.2021", "Сумма операции": -354.0},
            {"Дата операции": "29.09.2021", "Сумма операции": -2110.0},
            {"Дата операции": "29.08.2021", "Сумма операции": -25.0},
        ],
        50,
        "Такси",
    )
    print(spending_by_category("../data/operations.xls", "Фастфуд", "07.10.2018"))
