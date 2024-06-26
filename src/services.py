import pandas as pd
import re
import json
from datetime import datetime


def read_transactions_xlsx_file(xlsx_file: str) -> list[dict]:
    """Считывание финансовые операций с XLSX файла и возвращает DataFrame"""
    reader = pd.read_excel(xlsx_file)
    data = reader.to_dict(orient="records")
    return data


def analysis_of_cashback_categories(data: str, year: str, month: str) -> str:
    cashback_data = {}
    new_data = read_transactions_xlsx_file(data)
    user_date = datetime.strptime(f"{month}.{year}", "%m.%Y")
    print(user_date)
    for transaction in new_data:
        date_string = str(transaction.get("Дата операции", ""))
        if date_string != "nan":
            transaction_date = datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")
            if user_date.strftime('%m.%Y') in transaction_date.strftime('%m.%Y'):
                cashback_data[transaction.get("Категория")] = transaction.get("Бонусы (включая кэшбэк)")
                for k, v in cashback_data.items():
                    if k == transaction.get("Категория"):
                        cashback_data[transaction.get("Категория")] += transaction.get("Бонусы (включая кэшбэк)")

    print(cashback_data)


analysis_of_cashback_categories("../data/operations.xls", "2018", "5")


# def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
#     pass


def simple_search(user_request: str) -> str:
    """Функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос пользователя в описании или категории."""
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        if (user_request.lower() in (transaction.get("Описание", "")).lower()) or user_request.lower() in (
                str(transaction.get("Категория", ""))).lower():
            data.append(transaction)
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data


# print(simple_search("Такси"))


def transfer_to_individuals() -> str:
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам."""
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        for k, v in transaction.items():
            if v == "Переводы" and k == "Категория":
                if re.match(r'\D+\s\D?\.', f'{transaction.get("Описание", "")}'):
                    data.append(transaction)
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data


# print(transfer_to_individuals())


def sort_by_phone_numbers() -> str:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        if re.match(r'\D+\s?\D*\s\W\d\s\d+\s\d+\W\d+\W\d+', f'{transaction.get("Описание", "")}'):
            data.append(transaction)
    json_data = json.dumps(data, ensure_ascii=False)

    return json_data

# print(sort_by_phone_numbers())
