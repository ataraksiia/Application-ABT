from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.logger import setup_logger
from src.services import read_transactions_xlsx_file

logger = setup_logger("reports", "../all_loggers/reports.log")


def spending_by_category(transactions: str, category: str, date: Optional[str] = None) -> pd.DataFrame:
    logger.info("start spending_by_category")
    category = category.title()
    expenditure = []
    if date is not None:
        format_date = datetime.strptime(f"{date}", "%d.%m.%Y")
    else:
        format_date = datetime.now()
    date_3_month_ago = format_date - timedelta(days=90)
    data = read_transactions_xlsx_file(transactions)
    # print(data)
    for transaction in data:
        if pd.isnull(transaction.get("Дата платежа", "")) is False and transaction.get("Категория", "") == category:
            if (
                date_3_month_ago
                <= datetime.strptime(f'{transaction.get("Дата платежа", "")}', "%d.%m.%Y")
                <= format_date
            ):
                expenditure.append(
                    {
                        "Дата платежа": transaction.get("Дата платежа", ""),
                        "Категория": transaction.get("Категория", ""),
                        "Сумма платежа": transaction.get("Сумма платежа", ""),
                    }
                )

    df = pd.DataFrame(list(expenditure), columns=["Дата платежа", "Категория", "Сумма платежа"])
    logger.info(f"end \n{df}\n")
    return df


print(spending_by_category("../data/operations.xls", "Фастфуд", "07.10.2018"))
