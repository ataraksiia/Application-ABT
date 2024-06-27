import json
import math
import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


def read_transactions_xlsx_file(xlsx_file: str) -> list[dict]:
    """Считывание финансовые операций с XLSX файла и возвращает DataFrame"""
    reader = pd.read_excel(xlsx_file)
    data = reader.to_dict(orient="records")
    return data


def analysis_of_cashback_categories(data: str, year: str, month: str) -> str:
    """Функция для анализа выгодности категорий повышенного кешбэка."""
    cashback_data = {}
    new_data = read_transactions_xlsx_file(data)
    user_date = datetime.strptime(f"{month}.{year}", "%m.%Y")
    for transaction in new_data:
        date_string = str(transaction.get("Дата операции", ""))
        if date_string != "nan":
            transaction_date = datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")
            if user_date.strftime("%m.%Y") in transaction_date.strftime("%m.%Y"):
                if transaction.get("Категория") not in cashback_data:
                    cashback_data[transaction.get("Категория")] = transaction.get("Бонусы (включая кэшбэк)")
                else:
                    cashback_data[transaction.get("Категория")] += transaction.get("Бонусы (включая кэшбэк)")

    json_data = json.dumps(cashback_data, ensure_ascii=False)
    return json_data


# print(analysis_of_cashback_categories("../data/operations.xls", "2018", "12"))
def rounded_number(num: int, step: int) -> int:
    """Функция округления числа с определённым шагом"""
    plus_num = (num**2) ** 0.5
    round_number = int(math.ceil(plus_num / step)) * step
    return round_number


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Функция, которая возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    money_box = 0
    user_date = datetime.strptime(f"{month}", "%Y-%m")
    for transaction in transactions:
        date_string = transaction.get("Дата операции", "")
        if date_string != "":
            transaction_date = datetime.strptime(date_string, "%d.%m.%Y")
            if user_date.strftime("%m.%Y") in transaction_date.strftime("%m.%Y"):
                money_box += (
                    rounded_number(transaction.get("Сумма операции", ""), limit)
                    - (transaction.get("Сумма операции", "") ** 2) ** 0.5
                )
    return money_box


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


def simple_search(user_request: str) -> str:
    """Функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос пользователя в описании/категории."""
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        if (user_request.lower() in (transaction.get("Описание", "")).lower()) or user_request.lower() in (
            str(transaction.get("Категория", ""))
        ).lower():
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
                if re.match(r"\D+\s\D?\.", f'{transaction.get("Описание", "")}'):
                    data.append(transaction)
    json_data = json.dumps(data, ensure_ascii=False)
    return json_data


# print(transfer_to_individuals())


def sort_by_phone_numbers() -> str:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        if re.match(r"\D+\s?\D*\s\W\d\s\d+\s\d+\W\d+\W\d+", f'{transaction.get("Описание", "")}'):
            data.append(transaction)
    json_data = json.dumps(data, ensure_ascii=False)

    return json_data


# print(sort_by_phone_numbers())
