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
today_str = today.strftime("%d-%m-%Y")
today_obj = datetime.strptime(today_str, "%d-%m-%Y")
console = Console()
table = Table(title="Superpy Report")


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
    if (len(amount)) == 0:
        print('total profit of', parsed_arg.date, '=', '€', (sum(amount)))
    else:
        rich_visual(items)
        print('total profit of', parsed_arg.date, '=', '€', (sum(amount)))


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
    if (len(amount)) == 0:
        print('total revenue of', parsed_arg.date, '=', '€', (sum(amount)))
    else:
        rich_visual(items)
        print('total revenue of', parsed_arg.date, '=', '€', (sum(amount)))


def stock_report(parsed_arg):
    items = []
    with open("bought.csv", 'r') as file_in:
        reader = csv.DictReader(file_in)
        for row in reader:
            dt_obj1 = datetime.strptime(row['Expiration Date'], "%d-%m-%Y")
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


def rich_visual(items):
    for heading in items[0]:
        table.add_column(f"{heading}")
    for row in items:
        table.add_row(*row.values())
    console = Console()
    console.print(table)


def update_bought_csv(joinedlist):
    with open('bought.csv', "w") as file_out:
        writer = csv.writer(file_out, delimiter=',',
                            quotechar=',', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        for line in joinedlist:
            writer.writerow(line)
    file_out.close()


def update_sold_csv(sell, parsed_arg):
    sold_to_list = [*[list(idx.values()) for idx in sell]]
    profit = parsed_arg.price - float(sold_to_list[0][3])
    merged_sell_data = [parsed_arg.id, parsed_arg.product, today_str,
                        float(sold_to_list[0][3]), parsed_arg.price, profit]
    with open('sold.csv', "a", newline="") as file_out:
        writer = csv.writer(file_out, delimiter=',', quotechar=',')
        writer.writerow(merged_sell_data)
    file_out.close()


def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.strptime(arg_date_str, "%d-%m-%Y")
    except ValueError as exc:
        msg = f"Given Expiration Date ({arg_date_str}) is not valid! Expected format, \
DD-MM-YYYY!".format(arg_date_str)
        raise argparse.ArgumentTypeError(msg) from exc


def rest_key_value(parsed_arg):
    key_list = list(WARES.keys())
    val_list = list(WARES.values())
    position = val_list.index(parsed_arg.product)
    parsed_arg.id = key_list[position]
    return parsed_arg


WARES = {'01': "orange", '02': "banana", '03': "milk", '04': "cookies", '05': "toothpaste"}

DATES = ["today", "yesterday", "this-week", "last-week", "this-month", "this-year"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Welcome to Superpy inventory manager!")
    subparsers = parser.add_subparsers()

    # Create a showtop20 subcommand
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

    # Create a listapps subcommand
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
    parser_stock.set_defaults(func=stock_report)

# Print usage message if no args are supplied.

# NOTE: Python 2 will error 'too few arguments' if no subcommand is supplied.
#       No such error occurs in Python 3, which makes it feasible to check
#       whether a subcommand was provided (displaying a help message if not).
#       argparse internals vary significantly over the major versions, so it's
#       much easier to just override the args passed to it.

    if len(sys.argv) <= 3:
        sys.argv.append('--help')

    parsed_arg = parser.parse_args()

# Run the appropriate function (in this case showtop20 or listapps)
    parsed_arg.func(parsed_arg)

# If you add command-line options, consider passing them to the function,
# e.g. `options.func(options)`
