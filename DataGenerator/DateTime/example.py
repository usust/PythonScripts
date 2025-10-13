from date import *

if __name__ == "__main__":
    dates = generate_date_range("2020-03-01", "2020-03-10", date_format="%Y-%m-%d", quantity=20)
    for date in dates:
        print(date)
