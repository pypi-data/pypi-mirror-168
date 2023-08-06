import datetime
import calendar


class CalendarCalc:

    def __init__(self):
        pass

    def weekday_count(self, start, end, format):
        start_date = datetime.datetime.strptime(start, format)
        end_date = datetime.datetime.strptime(end, format)
        week = {}
        for i in range((end_date - start_date).days + 1):
            day = calendar.day_name[(start_date + datetime.timedelta(days=i)).weekday()]
            week[day] = week[day] + 1 if day in week else 1
        return week


if __name__ == '__main__':
    CC = CalendarCalc()
    format = '%Y-%m-%d'
    start = "2022-08-01"
    end = "2022-08-31"

    a = CC.weekday_count(start, end, format)
    print(a)
