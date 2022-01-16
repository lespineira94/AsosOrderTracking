# AsosOrderTracking

This script is made for people who want to declare their earnings and keep track of all their orders in the ASOS app.
It tracks all the orders you want and then exports it to an excel file based in the Cointracker excel

# Installation

First install [Python](https://www.python.org/downloads/) and the following dependencies:

## BeautifulSoup4
This enables to scrap html from the web
```sh
pip install beautifulsoup4
```
## Pandas
For datasets management and exports

```sh
pip install pandas
```

After all depdencies are installed we have to take the html code of the orders to scrapp and process all the orders and create a file named orders.txt with the html. The script will process only the orders we see on screen, so you will need to scroll down all the orders you want to process
So first we go to the orders tab and right click and go to inspect:
![image](https://user-images.githubusercontent.com/96527883/149680623-ca4d4433-c472-477e-a008-85371b9bc44f.png)

Right click on the htlm tag and go to  "Edit as HTML", 
![image](https://user-images.githubusercontent.com/96527883/149681600-55ec6269-1e3c-4a17-8154-236e2c4c2ae0.png)
It opens the following tab and we copy all the htlm code using CTRL+A and CTRL+C 
![image](https://user-images.githubusercontent.com/96527883/149681789-bfab73dc-4cf8-4307-8b16-4ab114d2e567.png).
Next we create a file named "orders.txt" in the same folder of the script and we paste all the code we have copied into the file:
![image](https://user-images.githubusercontent.com/96527883/149681923-3b91dce6-2527-4e27-ad8f-8ab29fadc3cf.png)
Finally all we have to do is to open a terminal in the same directory of the AsosOrderTracking.py script and the orders.txt and run the following comand:
```sh
python .\AsosFIFO.py
```
If you only want to export orders from a specific date to the most recent date, we can indicate the start date to the script with the following option --sd:
```sh
python .\AsosFIFO.py --sd 2022-01-13
```
This will export only dates from day 13 included, to the most recent order date
There are other usefull parameters like:
* ```-f or --fn```. To indicate a specific filename to the ".txt" file that we want to procces (by default it will be "orders.txt")
* ```-e or --fe```. To indicate the excel filename (by default "ordersData.xlsx")
 
Once we run the script we will get an excel with the resume of all of our buys and sells, comissions and prices of the orders that we did in the aplication:

![image](https://user-images.githubusercontent.com/96527883/149682705-a107a7f9-9d09-4d27-9af6-0e75720d41db.png)
