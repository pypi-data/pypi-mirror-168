""" shared utilities """
from datetime import datetime
import logging
from typing import List
from bs4 import BeautifulSoup, ResultSet, Tag
from .const import (
    CONNECTION_SPEED,
    DOWNLOAD,
    EXTRA_CONSUMPTION,
    LAST_UPDATE,
    QUOTA,
    TOTAL_CONSUMPTION,
    UPLOAD,
)
from .types import Account, Bill, BillInfo, BillStatus, Content, ConsumptionInfo


def __parse_status_value(str_val: str):
    val = str_val.split()[0]

    if val == "Unlimited":
        return float("inf")
    else:
        return float(val)


def parse_content(content: Content):
    """
    convert html into soup
    """
    return BeautifulSoup(content, "html.parser")


def parse_consumption_info(content: Content) -> ConsumptionInfo:

    info = ConsumptionInfo()
    statuses = parse_content(content).find_all(class_="MyConsumptionGrid")

    for status_div in statuses:
        [key, value] = [span.text.strip() for span in status_div]

        if key == CONNECTION_SPEED:
            info.speed = value
        elif key == QUOTA:
            info.quota = __parse_status_value(value)
        elif key == UPLOAD:
            info.upload = __parse_status_value(value)
        elif key == DOWNLOAD:
            info.download = __parse_status_value(value)
        elif key == TOTAL_CONSUMPTION:
            info.total_consumption = __parse_status_value(value)
        elif key == EXTRA_CONSUMPTION:
            info.extra_consumption = __parse_status_value(value)
        elif key == LAST_UPDATE:
            info.last_update = datetime.strptime(value, "%B %d,%Y  %H:%M")

    return info


def parse_accounts(content: Content) -> List[Account]:

    accounts: List[Account] = []

    account_options = (
        parse_content(content).find("select", id="changnumber").find_all("option")
    )

    for account_option in account_options:

        account = Account()
        account.phone = account_option.attrs["value"]
        account.internet = account_option.attrs["value2"]

        accounts.append(account)

    return accounts


def parse_bills(content: Content) -> BillInfo:

    bill_info = BillInfo()

    bill_info.total_outstanding = (
        parse_content(content)
        .find(class_="BillOutstandingSection1")
        .find("span")
        .get_text(strip=True)
    )

    logging.debug(f"outstanding {bill_info.total_outstanding}")

    bill_table = parse_content(content).find("table", class_="BillTable")
    bill_rows: List[Tag] = bill_table.find_all("tr")

    # logging.debug(f"table {bill_table}")

    for row in bill_rows:

        bill = Bill()
        col_date = row.find(class_="BillDate")
        if col_date is None:
            continue
        date_text = col_date.get_text(strip=True)
        bill.date = datetime.strptime(date_text, "%b%Y")

        logging.debug(f"################################")
        logging.debug(f"date: {bill.date.strftime('%b %Y')}")

        col_amount = row.find(class_="BillAmount")
        bill.amount = col_amount.get_text(strip=True)
        logging.debug(f"amount: {bill.amount}")

        col_status = col_amount.parent.findNextSibling("td")
        status = col_status.get_text(strip=True).lower()
        if status == "paid":
            bill.status = BillStatus.PAID
        elif status == "not paid":
            bill.status = BillStatus.UNPAID
        else:
            bill.status = BillStatus.UNKNOWN
        logging.debug(f"status: {bill.status}")

        bill_info.bills.append(bill)

    logging.debug(f"################################")

    return bill_info


def parse_error_message(content: Content):

    script_tag = (
        parse_content(content)
        .find("script", {"language": "javascript"})
    )

    if script_tag is None:
        return None

    msg = (
        script_tag
        .get_text(strip=True)
    )

    err_idx = msg.find("error=")
    if err_idx == -1:
        return None

    err_msg = msg[err_idx + 6:]
    err_msg = err_msg.split("&")[0]
    err_msg = err_msg.split(";")[0]
    err_msg = err_msg.split("\"")[0]

    return err_msg
