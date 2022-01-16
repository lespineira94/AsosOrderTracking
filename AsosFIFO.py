from enum import Enum
from bs4 import BeautifulSoup

import pandas as pd
import getopt
import sys


class SaleInfo():
    def __init__(self, realPrice, comision):
        self.realPrice = realPrice
        self.comision = comision
        self.totalPrice = float(realPrice) + float(comision)


class OrderType(Enum):
    TRADE = 1
    DEPOSIT = 2
    WITHDRAW = 3


def findOrderId(order):
    orderId = order.find(
        "div", class_="order-num").find("span", class_="value")

    # Replaces order with empty because we only need the orderId
    return orderId.text.replace("order", "")


def findSaleInfo(order):
    sale = order.findAll("div", class_="money-item flex-btw-center")

    # Gets the prices and replaces the $ symbol
    realPrice = sale[0].find("span", class_="num").text.replace("$", "")
    comision = sale[1].find("span", class_="num").text.replace("$", "")

    return SaleInfo(realPrice, comision)


def exportToExcel(exceldata, fileNameToExport):
    dataFrame = pd.DataFrame(exceldata)
    writer = pd.ExcelWriter(fileNameToExport, engine='xlsxwriter')

    dataFrame.to_excel(writer, index=False)

    writer.save()


def processOrders(htmlOrders, fileNameToExport):
    orderTypes = list()
    orderIds = list()
    dates = list()
    realPrices = list()
    comisions = list()
    totalPrices = list()

    # Process all the orders
    for order in htmlOrders:
        # Type. All orders will be operations for the moment
        orderTypes.append(OrderType.TRADE.name)

        # Order id
        orderId = findOrderId(order)
        orderIds.append(orderId)

        # Date
        date = order.find("span", class_="value").text
        dates.append(date)

        saleInfo = findSaleInfo(order)

        # Real price
        realPrice = saleInfo.realPrice
        realPrices.append(realPrice)

        # Comision
        comision = saleInfo.comision
        comisions.append(comision)

        # Total price (price + comision)
        totalPrice = saleInfo.totalPrice
        totalPrices.append(totalPrice)

    exceldata = {
        "Type": orderTypes,
        "Order Id": orderIds,
        "Buy": realPrices,
        "Sell": totalPrices,
        "Comision": comisions,
        "Currency": "USDT",
        "Date": dates
    }

    exportToExcel(exceldata, fileNameToExport)

    print("Orders exported succesfully")

    file.close()


try:
    fileToProcess = "orders.txt"
    fileNameToExport = "ordersData.xlsx"

    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "f:e:")

    for opt, arg in opts:
        if opt in ["-f"]:
            fileToProcess = arg
        elif opt in ["-e"]:
            fileNameToExport = arg

    file = open(fileToProcess)
    soup = BeautifulSoup(file.read(), "html.parser")

    htmlOrders = soup.findAll("li", class_="task-item")

    processOrders(htmlOrders, fileNameToExport)


except FileNotFoundError:
    print("File " + fileToProcess + " not found.")
except PermissionError:
    print("You have to close your current open excel to export new data")
