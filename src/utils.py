from datetime import datetime


def get_timestamp(date: str) -> str:
    date_lst = date.split(" ")
    month_name = date_lst[2]
    day_num = date_lst[3]
    year = date_lst[4]
    hour_12h = date_lst[5]
    flag = date_lst[6]

    month = ""
    match month_name:
        case "Jan":
            month = "1"
        case "Feb":
            month = "2"
        case "Mar":
            month = "3"
        case "Apr":
            month = "4"
        case "May":
            month = "5"
        case "Jun":
            month = "6"
        case "Jul":
            month = "7"
        case "Aug":
            month = "8"
        case "Sep":
            month = "9"
        case "Oct":
            month = "10"
        case "Nov":
            month = "11"
        case "Dec":
            month = "12"

    day = ""
    if day_num[:2].isnumeric():
        day = day_num[:2]
    else:
        day = day_num[0]

    if flag == "PM":
        hour = int(hour_12h.split(":")[0]) + 12 % 24
    else:
        hour = int(hour_12h.split(":")[0])

    minutes = int(hour_12h.split(":")[1])
    dtime = datetime(int(year), int(month), int(day), hour, minutes)

    return str(dtime.timestamp())
