import jdatetime


def convert_to_jalali_date(gregorian_date):
    return jdatetime.date.fromgregorian(date=gregorian_date)