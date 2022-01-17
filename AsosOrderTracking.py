from enum import Enum
from bs4 import BeautifulSoup
from datetime import datetime

import pandas as pd
import getopt
import sys


class SaleInfo():
    def __init__(self, realPrice, comision):
        self.realPrice = realPrice
        self.comision = comision
        self.totalPrice = float(realPrice) + float(comision)


class ProgramArguments():
    def __init__(self, fileToProcess, fileNameToExport, startDate):
        self.fileToProcess = fileToProcess
        self.filenameToExport = fileNameToExport
        self.startDate = startDate

    def __str__(self):
        return "FileToProcess: " + self.fileToProcess + " FileNameToExport: " + self.filenameToExport + " StartDate: " + str(self.startDate)


class OrderType(Enum):
    TRADE = 1
    DEPOSIT = 2
    WITHDRAW = 3


def getProgramArguments():
    fileToProcess = "orders.txt"
    fileNameToExport = "ordersData.xlsx"
    startDate = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(
            argv, "f:e:s:", ["fn=", "fe=", "sd="])

        for opt, arg in opts:
            if opt in ["-f", "--fn"]:
                fileToProcess = arg
            elif opt in ["-e", "--fe"]:
                fileNameToExport = arg
            elif opt in ["-s", "--sd"]:
                startDate = datetime.strptime(arg, "%Y-%m-%d")
    except getopt.GetoptError as e:
        print("ERROR: ", e)

    return ProgramArguments(fileToProcess, fileNameToExport, startDate)


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

    print("Orders exported succesfully")


def checkOrderToProcess(startDate, orderDate):
    orderDateTime = datetime.strptime(orderDate, "%Y-%m-%d %H:%M:%S")

    return startDate == None or orderDateTime >= startDate


def processOrders(htmlOrders, programArguments):
    orderTypes = list()
    orderIds = list()
    dates = list()
    realPrices = list()
    comisions = list()
    totalPrices = list()

    # Process all the orders
    for order in htmlOrders:
        # Date
        orderDate = order.find("span", class_="value").text

        # Checks if the order has to be processed when we are filtering by dates
        processOrder = checkOrderToProcess(
            programArguments.startDate, orderDate)

        if processOrder == True:
            dates.append(orderDate)

            # Type. All orders will be operations for the moment
            orderTypes.append(OrderType.TRADE.name)

            # Order id
            orderId = findOrderId(order)
            orderIds.append(orderId)

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

    # Columns and values for the excel
    exceldata = {
        "Type": orderTypes,
        "Order Id": orderIds,
        "Buy": realPrices,
        "Sell": totalPrices,
        "Comision": comisions,
        "Currency": "USDT",
        "Date": dates
    }

    # Exports the orders data to excel
    exportToExcel(exceldata, programArguments.filenameToExport)

    file.close()


try:
    programArguments = getProgramArguments()

    # Opens the .txt with the html code
    file = open(programArguments.fileToProcess)
    soup = BeautifulSoup(file.read(), "html.parser")

    # Gets all the orders in the html
    htmlOrders = soup.findAll("li", class_="task-item")

    processOrders(htmlOrders, programArguments)


except FileNotFoundError:
    print("File " + programArguments.fileToProcess + " not found.")
except PermissionError:
    print("You have to close your current open excel to export new data")
