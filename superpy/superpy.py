"""AMENABILLITY:
Requrements of assignment = The application must support:

1. Setting and advancing the date that the application perceives as 'today';
Setting and advancing time date is implemented as follows:
the program compares the input dates relatively to today.datetime given by user
with entries in the stored.csv and sold.csv files
as for advancing the time:

In the setup of superpy this feature only makes sence to check future stock.
Items that will have expired on the advance time date -can be set by int or date input-
are not shown as stock in the reportstock since that is the only certainty.
for example: 
python superpy.py report stock -d today -a 1 --will give you tomorrow's stock while
python superpy.py report stock -d today -a 20-03-2023 --will give you the stock on certain date

2. Recording the buying and selling of products on certain dates;
this is handled by the buying and selling functions of superpy. bought items are being
logged in bought.csv. Sold items are removed from bought csv and after profit count stored in sold.csv 
with a date stamp

3. Reporting revenue and profit over specified time periods;
this is handled by the report profit and report revenue functions of superpy. revenue and profit reports 
can only be written for past or current dates. 

4. Exporting selections of data to CSV files;
All report functions (revenue, profit and stock) give user the option to store the given quary result in
stored.csv. The entry's in stored.csv are written with custom headers for the data that is stored and
provided with a timestamp to provide easy look-up in stored.csv

5. Two other additional non-trivial features of your choice, for example:
6. The use of an external module Rich(opens in a new tab) to improve the application.
7. The ability to import/export reports from/to formats other than CSV (in addition to CSV)
8. The ability to visualize some statistics using Matplotlib(opens in a new tab)
9. Another feature that you thought of.

- This program make use of the rich visual library for reports and stock mutations.
- This program has a build in feature that saves the user money buy always selling 
the stock that will expire first"""


# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=missing-module-docstring
# pylint: disable=unspecified-encoding - W1514


# Imports
import argparse
import csv
from datetime import date, timedelta, datetime
import sys
from rich.console import Console
from rich.table import Table


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
today = date.today()
now = datetime.now()
now_str = now.strftime("%d-%m-%Y-%T")
today_str = today.strftime("%d-%m-%Y")
today_obj = datetime.strptime(today_str, "%d-%m-%Y")
console = Console()
table = Table(title="Superpy Report")


# This function takes in the parsed arguments from the command line and logs
# the purchase information into a CSV file.
# NOTE: The function also prints a message indicating that the purchase has been logged


def buy(parsed_arg):
    parsed_arg = rest_key_value(parsed_arg)
    start_datetime_object = parsed_arg.start_datetime
    end_datetime_object = parsed_arg.end_datetime
    start_date = datetime.date(start_datetime_object)
    start_date_str = start_date.strftime("%d-%m-%Y")
    end_date = datetime.date(end_datetime_object)
    end_date_str = end_date.strftime("%d-%m-%Y")
    with open('bought.csv', "a", newline="") as file_out:
        buy_path_data = [parsed_arg.id, parsed_arg.product, start_date_str,
                         parsed_arg.cost, end_date_str]
        writer = csv.writer(file_out, delimiter=',')
        writer.writerow(buy_path_data)
        file_out.close()
    buy_path_close_text = f" The {parsed_arg.product} bought on {start_date_str} for \
Є{parsed_arg.cost}- and expires on {end_date_str} is logged!"
    print(buy_path_close_text)
    file_out.close()

# This function takes in the parsed arguments from the command line and searches the bought.csv 

# NOTE: file for products that match the given ID. If there are no items that match the given ID, 
# an error message is printed. If there are items that match the given ID, 
# the function determines which one has the earliest expiration date and logs the sale into a CSV file.
# The function then updates the bought.csv file to remove the item that was sold.
# In case there is no product to be sold the user is informed. In case there is not product to be sold
# with experation date after the day before the items that are expired are shown to the user.

def sell(parsed_arg):
    parsed_arg = rest_key_value(parsed_arg)
    with open("bought.csv", 'r') as file_in:
        reader = csv.DictReader(file_in)
        is_expired = []
        rows = []
        for row in reader:
            if row['Product id'] == parsed_arg.id:
                dt_obj1 = datetime.strptime(row['Expiration Date'], "%d-%m-%Y")
                if dt_obj1 >= today_obj:
                    rows.append(row)
                elif row['Product id'] == parsed_arg.id:
                    is_expired.append(row)
        expired_list = [*[list(idx.values()) for idx in is_expired]]
        if (len(rows)) == 0 and len(is_expired) == 0:
            print("***ERROR: Out Of", parsed_arg.product, '`s', "[", len(is_expired),
                  "] items expired ***")
            return
        if (len(rows)) == 0 and len(is_expired) > 0:
            rich_visual(is_expired)
            print("***ERROR: Out Of", parsed_arg.product, '`s', "[", len(is_expired),
                  "] items expired ***")
            return
        dates = []
        for item in rows:
            dates.append(item['Expiration Date'])
        if len(dates) > 1:
            keep = [item for item in rows if item['Expiration Date'] is not (min(dates))]
            sell = [item for item in rows if item['Expiration Date'] is (min(dates))]
            items = sell
            rich_visual(items)
        else:
            keep = [item for item in rows if item['Expiration Date'] is (min(dates[0]))]
            sell = [item for item in rows if item['Expiration Date'] is (min(dates))]
            items = sell
            rich_visual(items)
        update_sold_csv(sell, parsed_arg)
        print("--Sold-- a", parsed_arg.product, "with a date of", (min(dates)),
              "The Current Stock =", "[", len(rows) - 1, "]")
        merge_list = [*[list(idx.values()) for idx in keep]]
        backup = combine_list()
        joinedlist = backup + merge_list + expired_list
        update_bought_csv(joinedlist)

# This function takes in the parsed arguments from the command line and calculates 
# the total profit for products sold within the given time period. 
# NOTE: The function reads the sold.csv file to obtain information about products 
# that were sold and when they were sold. 
# The function then calculates the profit for each sale and sums up the profits 
# for all sales within the given time period. 
# Finally, the function prints a report of the total profit earned within the given time period.


def profit_report(parsed_arg):
    items = []
    amount = []
    with open("sold.csv", 'r') as file_in:
        reader = csv.DictReader(file_in)
        for row in reader:
            dt_obj1 = datetime.strptime(row['Sell Date'], "%d-%m-%Y")
            if parsed_arg.date == 'today':
                if dt_obj1 == today_obj:
                    amount.append(float(row['Profit']))
                    items.append(row)
            if parsed_arg.date == 'yesterday':
                yesterday = today_obj - timedelta(1)
                if dt_obj1 < today_obj >= yesterday:
                    amount.append(float(row['Profit']))
                    items.append(row)
            if parsed_arg.date == 'this-week':
                last_monday = today_obj - timedelta(days=now.weekday())
                next_sunday = last_monday + timedelta(days=6)
                if last_monday <= dt_obj1 <= next_sunday:
                    amount.append(float(row['Profit']))
                    items.append(row)
            if parsed_arg.date == 'last-week':
                last_week_monday = today_obj - timedelta(weeks=1, days=now.weekday())
                last_sunday = last_week_monday + timedelta(days=6)
                if last_week_monday <= dt_obj1 <= last_sunday:
                    amount.append(float(row['Profit']))
                    items.append(row)
            if parsed_arg.date == 'this-month':
                fst_month = now.replace(day=1)
                if dt_obj1 >= fst_month <= today_obj:
                    amount.append(float(row['Profit']))
                    items.append(row)
            if parsed_arg.date == 'this-year':
                fst_year = now.replace(day=1, month=1)
                if dt_obj1 >= fst_year <= today_obj:
                    amount.append(float(row['Profit']))
                    items.append(row)
        if (len(items)) > 0:
            rich_visual(items)
            print('total profit', parsed_arg.date, '=', 'Є', (sum(amount)))
            user_input = input('store this query result?(y/n): ')
            if user_input.lower() == 'y':
                save_quary(items)
                print('query result stored in: stored.csv')
            elif user_input.lower() == 'n':
                return
        if (len(items)) == 0:
            print('total revenue', parsed_arg.date, '=', 'Є', (sum(amount)))

# This function takes in the parsed arguments from the command line and calculates 
# the total revenue for products sold within the given time period. 
# NOTE: The function reads the sold.csv file to obtain information about products 
# that were sold and when they were sold. 
# The function then calculates the revenue for each sale and sums up the revenue 
# for all sales within the given time period. 
# Finally, the function prints a report of the total revenue earned within the given time period.

def revenue_report(parsed_arg):
    items = []
    amount = []
    with open("sold.csv", 'r') as file_in:
        reader = csv.DictReader(file_in)
        for row in reader:
            dt_obj1 = datetime.strptime(row['Sell Date'], "%d-%m-%Y")
            if parsed_arg.date == 'today':
                if dt_obj1 == today_obj:
                    amount.append(float(row['Sell Price']))
                    items.append(row)
            if parsed_arg.date == 'yesterday':
                yesterday = today_obj - timedelta(1)
                if dt_obj1 < today_obj >= yesterday:
                    amount.append(float(row['Sell Price']))
                    items.append(row)
            if parsed_arg.date == 'this-week':
                last_monday = today_obj - timedelta(days=now.weekday())
                next_sunday = last_monday + timedelta(days=6)
                if last_monday <= dt_obj1 <= next_sunday:
                    amount.append(float(row['Sell Price']))
                    items.append(row)
            if parsed_arg.date == 'last-week':
                last_week_monday = today_obj - timedelta(weeks=1, days=now.weekday())
                last_sunday = last_week_monday + timedelta(days=6)
                if last_week_monday <= dt_obj1 <= last_sunday:
                    amount.append(float(row['Sell Price']))
                    items.append(row)
            if parsed_arg.date == 'this-month':
                fst_month = now.replace(day=1)
                if dt_obj1 >= fst_month <= today_obj:
                    print(row)
                    amount.append(float(row['Sell Price']))
                    items.append(row)
            if parsed_arg.date == 'this-year':
                fst_year = now.replace(day=1, month=1)
                if dt_obj1 >= fst_year <= today_obj:
                    amount.append(float(row['Sell Price']))
                    items.append(row)
        if (len(items)) > 0:
            rich_visual(items)
            print('total revenue', parsed_arg.date, '=', 'Є', (sum(amount)))
            user_input = input('store this query result?(y/n): ')
            if user_input.lower() == 'y':
                save_quary(items)
                print('query result stored in: stored.csv')
            elif user_input.lower() == 'n':
                return
        if (len(items)) == 0:
            print('total revenue', parsed_arg.date, '=', 'Є', (sum(amount)))

# This function takes in the parsed arguments from the command line and compares
# which items are valid by expiration date given time period. 
# NOTE: The function reads the bought csv file and looks which items have an
# expiration date that is higher than the given time period. 
# additionally the function can take an advance time argument to set days up by input 
# for example five days is (-adv-time 5) or set a specific date for example 30-12-2023
# after the quary results is given in visualisation with rich visuals user has the
# option to have the quary results being written to stored csv which the program will
# do with taking in to account necessary headers for different routes and a timestamp 
# of the quary


def stock_report(parsed_arg):
    items = []
    with open("bought.csv", 'r') as file_in:
        reader = csv.DictReader(file_in)
        adv_time = verify_input(parsed_arg)
        for row in reader:
            dt_obj1 = datetime.strptime(row['Expiration Date'], "%d-%m-%Y")
            if parsed_arg.adv_time is not None and dt_obj1 >= adv_time:
                items.append(row)
            if parsed_arg.date == 'today':
                if dt_obj1 >= today_obj:
                    items.append(row)
            if parsed_arg.date == 'yesterday':
                yesterday = today_obj - timedelta(1)
                if dt_obj1 >= yesterday:
                    items.append(row)
            if parsed_arg.date == 'this-week':
                last_monday = now - timedelta(days=now.weekday())
                if dt_obj1 >= last_monday:
                    items.append(row)
            if parsed_arg.date == 'last-week':
                last_monday = now - timedelta(days=now.weekday())
                last_week = last_monday - timedelta(1)
                if dt_obj1 >= last_week:
                    items.append(row)
            if parsed_arg.date == 'this-month':
                fst_month = now.replace(day=1)
                if dt_obj1 >= fst_month <= today_obj:
                    items.append(row)
            if parsed_arg.date == 'this-year':
                fst_year = now.replace(day=1, month=1)
                if dt_obj1 >= fst_year <= today_obj:
                    items.append(row)
        if (len(items)) > 0:
            rich_visual(items)
            print('total in stock', parsed_arg.date, '=', (len(items)), 'items')
            user_input = input('store this query result?(y/n): ')
            if user_input.lower() == 'y':
                save_quary(items)
                print('query results stored in: stored.csv')
            elif user_input.lower() == 'n':
                return
        if (len(items)) == 0:
            print('total in stock', parsed_arg.date, '=', (len(items)), 'items')




def combine_list():
    with open("bought.csv", 'r') as file_in:
        key = [parsed_arg.id]
        reader = csv.reader(file_in)
        data = list(reader)
        backup = [x for x in data if key[0] not in x]
    file_in.close()
    return backup

# this function improves quary results by adding visual columns for the headers and their values 
# it uses the rich library
# NOTE: the reason for this is to given a more apealing experience and give more oversight on the
# data

def rich_visual(items):
    for heading in items[0]:
        table.add_column(f"{heading}")
    for row in items:
        table.add_row(*row.values())
    console = Console()
    console.print(table)

# this is the writer csv function for the buy-route


def update_bought_csv(joinedlist):
    with open('bought.csv', "w") as file_out:
        writer = csv.writer(file_out, delimiter=',',
                            quotechar=',', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        for line in joinedlist:
            writer.writerow(line)
    file_out.close()

# this is the writer csv function for the sell-route
# NOTE: it calculates the profits and makes a new list of requrements

def update_sold_csv(sell, parsed_arg):
    sold_to_list = [*[list(idx.values()) for idx in sell]]
    profit = parsed_arg.price - float(sold_to_list[0][3])
    merged_sell_data = [parsed_arg.id, parsed_arg.product, today_str,
                        float(sold_to_list[0][3]), parsed_arg.price, profit]
    with open('sold.csv', "a", newline="") as file_out:
        writer = csv.writer(file_out, delimiter=',', quotechar=',')
        writer.writerow(merged_sell_data)
    file_out.close()

#  this functions checks the date input from user on the buy-route to prevent
#  having the csv files get corrupted by date types superpy can't use. 
#  NOTE: it gives user the proper date for the program with example

def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.strptime(arg_date_str, "%d-%m-%Y")
    except ValueError as exc:
        msg = f"Given Expiration Date ({arg_date_str}) is not valid! Expected format, \
DD-MM-YYYY!".format(arg_date_str)
        raise argparse.ArgumentTypeError(msg) from exc

#  this functions checks the advance date input from user on the report stock-route 
#  advance time is optional argument. It checks if for existence and which format 
# the input is provided. 
# NOTE: In case of a date it tries to make a valid datetime object of the input
# if it can not format the format to date it sets the daytime object forward by the amount 
# of days provided by user

def verify_input(parsed_arg):
    if parsed_arg.adv_time is None:
        return parsed_arg
    try:
        adv_time = datetime.strptime(parsed_arg.adv_time[0], "%d-%m-%Y")
        parsed_arg.date = adv_time.strftime("%d-%m-%Y")
        return adv_time
    except ValueError:
        try:
            days = parsed_arg.adv_time[0]
            adv_time = today_obj + timedelta(int(days))
            parsed_arg.date = adv_time.strftime("%d-%m-%Y")
            return adv_time
        except ValueError as exc:
            msg = f"Given Expiration Date ({parsed_arg.adv_time[0]}) is not valid! Expected format: \
DD-MM-YYYY or (round)number for example(1)" 
            raise argparse.ArgumentTypeError(msg) from exc


# this function restores the product of choice with its given id.key
# NOTE: the reason for this is to not bother the user with necesarry choice of id's that are
# handled by superpy in the background and out of sight of the user

def rest_key_value(parsed_arg):
    key_list = list(WARES.keys())
    val_list = list(WARES.values())
    position = val_list.index(parsed_arg.product)
    parsed_arg.id = key_list[position]
    return parsed_arg

# this function writes quary of user on reports to stored.csv
# NOTE: it features dynamic headers and writes a timestamp for easy retreaval of data 
# within stored.csv

def save_quary(items):
    data = [*[list(idx.values()) for idx in items]]
    header = [[list(idx.keys()) for idx in items]]
    time_stamp = ['timestamp quary: ' + now_str] 
    with open('stored.csv', "a", newline="") as file_out:
        writer = csv.writer(file_out, delimiter=',',
                            quotechar=',', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(time_stamp)
        writer.writerow(header[0][0])
        for line in data:
            writer.writerow(line)
    file_out.close()

# products library used with choices of argparse


WARES = {'01': "orange", '02': "banana", '03': "milk", '04': "cookies", '05': "toothpaste"}

# set-dates library used with choices of argparse


DATES = ["today", "yesterday", "this-week", "last-week", "this-month", "this-year"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Welcome to Superpy inventory manager 1.1! --added: advance time and store reports features")
    subparsers = parser.add_subparsers()

    # Create subcommand
    parser_buy = subparsers.add_parser('buy',
                                       help='bought products')
    parser_buy.add_argument('-p', '--product',
                            type=str,
                            choices=WARES.values(),
                            required=True,
                            help="select a product")
    parser_buy.add_argument('-b', '--buy-date',
                            dest='start_datetime',
                            type=valid_date_type,
                            default=None, required=True,
                            help="buy date as in format DD-MM-YYYY:")
    parser_buy.add_argument('-c', '--cost',
                            type=float,
                            required=True,
                            help="product cost in Є:")
    parser_buy.add_argument('-d', '--exp-date',
                            dest='end_datetime',
                            type=valid_date_type,
                            default=None, required=True,
                            help="expiration date as in format DD-MM-YYYY:")
    parser_buy.set_defaults(func=buy)

    # Create sub subcommand
    parser_sell = subparsers.add_parser('sell',
                                        help='sell products')
    parser_sell.add_argument('-b', '--product',
                             type=str,
                             choices=WARES.values(),
                             required=True,
                             help="select a product")
    parser_sell.add_argument('-p', '--price',
                             type=float,
                             required=True,
                             help="product price in Є:")
    parser_sell.set_defaults(func=sell)

    # Create a listapps subcommand
    parser_report = subparsers.add_parser('report',
                                          help='print reports')
    subparser_one = parser_report.add_subparsers()
    parser_profit = subparser_one.add_parser('profit', help='report revenue')
    parser_profit.add_argument('-d', '--date',
                               type=str,
                               choices=DATES,
                               required=True,
                               help="select profit period")
    parser_profit.set_defaults(func=profit_report)
    parser_revenue = subparser_one.add_parser('revenue', help='report profit')
    parser_revenue.add_argument('-d', '--date',
                                type=str,
                                choices=DATES,
                                required=True,
                                help="select revenue period")
    parser_revenue.set_defaults(func=revenue_report)
    parser_stock = subparser_one.add_parser('stock', help='report stock')
    parser_stock.add_argument('-d', '--date',
                              type=str,
                              choices=DATES,
                              required=True,
                              help="select stock period")
    # creating optional advance time argument for report stock-route
    parser_stock.add_argument('-a', '--adv-time',
                              nargs=1,
                              type=str,
                              required=False,
                              help="advance time in days or DD-MM-YYYY:")
    parser_stock.set_defaults(func=stock_report)

# Print usage message if no args are supplied.

    if len(sys.argv) <= 3:
        sys.argv.append('--help')

    parsed_arg = parser.parse_args()

# Run the appropriate function (in this case listapps)
    parsed_arg.func(parsed_arg)
