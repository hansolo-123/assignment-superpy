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