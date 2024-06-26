import json
import math
import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from src.logger import setup_logger

logger = setup_logger("services", "services.log")


def read_transactions_xlsx_file(xlsx_file: str) -> list[dict]:
    """Считывание финансовые операций с XLSX файла и возвращает DataFrame"""
    reader = pd.read_excel(xlsx_file)
    data = reader.to_dict(orient="records")
    return data


def analysis_of_cashback_categories(data: str, year: str, month: str) -> str:
    """Функция для анализа выгодности категорий повышенного кешбэка."""
    logger.info("start analysis_of_cashback_categories")
    cashback_data = {}
    new_data = read_transactions_xlsx_file(data)
    user_date = datetime.strptime(f"{month}.{year}", "%m.%Y")
    for transaction in new_data:
        date_string = str(transaction.get("Дата операции", ""))
        if date_string != "NaN":
            transaction_date = datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")
            if user_date.strftime("%m.%Y") in transaction_date.strftime("%m.%Y"):
                if transaction.get("Категория") not in cashback_data:
                    cashback_data[transaction.get("Категория")] = transaction.get("Бонусы (включая кэшбэк)")
                else:
                    cashback_data[transaction.get("Категория")] += transaction.get("Бонусы (включая кэшбэк)")
        for k, v in transaction.items():
            if pd.isnull(v):
                transaction[k] = None

    json_data = json.dumps(cashback_data, ensure_ascii=False, indent=4)
    logger.info(f"end {json_data}\n")
    return json_data


def rounded_number(num: int, step: int) -> int:
    """Функция округления числа с определённым шагом"""
    plus_num = (num**2) ** 0.5
    round_number = int(math.ceil(plus_num / step)) * step
    return round_number


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Функция, которая возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    logger.info("start investment_bank")
    money_box = 0
    user_date = datetime.strptime(f"{month}", "%Y-%m")
    for transaction in transactions:
        date_string = transaction.get("Дата операции", "")
        if date_string != "":
            transaction_date = datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")
            if user_date.strftime("%Y-%m") in transaction_date.strftime("%Y-%m"):
                money_box += (
                    rounded_number(transaction.get("Сумма операции", ""), limit)
                    - (transaction.get("Сумма операции", "") ** 2) ** 0.5
                )
    logger.info(f"end {money_box}\n")
    return money_box


def simple_search(user_request: str) -> str:
    """Функция возвращает JSON-ответ со всеми транзакциями, содержащими запрос пользователя в описании/категории."""
    logger.info("start simple_search")
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        if (user_request.lower() in (transaction.get("Описание", "")).lower()) or user_request.lower() in (
            str(transaction.get("Категория", ""))
        ).lower():
            data.append(transaction)
        for k, v in transaction.items():
            if pd.isnull(v):
                transaction[k] = None
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info(f"end {json_data}\n")
    return json_data


def transfer_to_individuals() -> str:
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам."""
    logger.info("start transfer_to_individuals")
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        for k, v in transaction.items():
            if pd.isnull(v):
                transaction[k] = None
            if v == "Переводы" and k == "Категория":
                if re.match(r"\D+\s\D?\.", f'{transaction.get("Описание", "")}'):
                    data.append(transaction)
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info(f"end {json_data}\n")
    return json_data


def sort_by_phone_numbers() -> str:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    logger.info("start sort_by_phone_numbers")
    python_data = read_transactions_xlsx_file("../data/operations.xls")
    data = []
    for transaction in python_data:
        for k, v in transaction.items():
            if pd.isnull(v):
                transaction[k] = None
        if re.match(r"\D+\s?\D*\s\W\d\s\d+\s\d+\W\d+\W\d+", f'{transaction.get("Описание", "")}'):
            data.append(transaction)

    # data = data[~np.isnan(data)]
    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info(f"end {json_data}\n")

    return json_data


def main_function_services() -> None:
    """Функуия, которая обьединяет функции модуля services."""
    user_input = input(
        "Хотите ли вы проанализировать, какие категории были наиболее выгодными для выбора"
        " в качестве категорий повышенного кешбэка?Да/Нет\n"
    ).lower()
    if user_input == "да":
        year, month = input("Введите год и месяц через пробел (формат 2021 08)\n").split()
        print(analysis_of_cashback_categories("../data/operations.xls", year, month))
    user_input = input(
        "Хотите ли вы узнать сумму, которую удалось бы отложить в «Инвесткопилку»,"
        "если бы вы настроили шаг округления? Да/Нет\n"
    ).lower()
    if user_input == "да":
        month = input("Введите год и месяц (формат 2021-08)\n")
        limit = int(input("Введите шаг округления\n"))
        data = read_transactions_xlsx_file("../data/operations.xls")
        print(investment_bank(month, data, limit))

    user_input = input(
        "Хотите ли вы отфильтровать транзакции по слову, которое должно содержаться"
        "в описании или категории? Да/Нет\n"
    ).lower()
    if user_input == "да":
        user_request = input("Введите слово\n").lower()
        print(simple_search(user_request))

    user_input = input("Хотите ли вы отфильтровать транзакции по мобильным номерам? Да/Нет\n").lower()
    if user_input == "да":
        print(sort_by_phone_numbers())

    user_input = input(
        "Хотите ли вы отфильтровать транзакции, которые относятся к переводам физлицам?" "Да/Нет\n"
    ).lower()
    if user_input == "да":
        print(transfer_to_individuals())
