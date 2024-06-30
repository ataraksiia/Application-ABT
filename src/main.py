from src.reports import spending_by_category
from src.services import (
    analysis_of_cashback_categories,
    investment_bank,
    simple_search,
    sort_by_phone_numbers,
    transfer_to_individuals,
)
from src.views import home_page

if __name__ == "__main__":
    print(home_page("2020-12-12 05:59:59"))
    print(analysis_of_cashback_categories("../data/operations.xls", "2018", "12"))
    print(
        investment_bank(
            "2021-09",
            [
                {"Дата операции": "29.09.2021", "Сумма операции": -4429.0},
                {"Дата операции": "29.09.2021", "Сумма операции": -354.0},
                {"Дата операции": "29.09.2021", "Сумма операции": -2110.0},
                {"Дата операции": "29.08.2021", "Сумма операции": -25.0},
            ],
            50,
        )
    )
    print(simple_search("Такси"))
    print(transfer_to_individuals())
    print(sort_by_phone_numbers())
    print(spending_by_category("../data/operations.xls", "Фастфуд", "07.10.2018"))
