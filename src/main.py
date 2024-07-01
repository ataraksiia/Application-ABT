from src.reports import spending_by_category
from src.services import main_function_services
from src.views import home_page

if __name__ == "__main__":
    time = input("Введите время (формат YYYY-MM-DD HH:MM:SS)\n")
    print(home_page(time))
    main_function_services()
    user_input = input(
        "Хотите проанализировать ваши траты по заданной категории за последние три месяца "
        "(от переданной даты)? Да/Нет\n"
    ).lower()
    if user_input == "да":
        category = input("Введите категорию\n").lower()
        date = input("Введите дату (формат 10.08.2020)\n").lower()
        print(spending_by_category("../data/operations.xls", category, date))
