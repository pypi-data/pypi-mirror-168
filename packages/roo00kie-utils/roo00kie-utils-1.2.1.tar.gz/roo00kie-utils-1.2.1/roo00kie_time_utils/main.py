import datetime


# 格林威治时间+8小时变为上海时间
def time_str_handler(utc_str, utc_format, shanghai_format):
	utc = datetime.datetime.strptime(utc_str, utc_format)
	shanghai = utc + datetime.timedelta(hours=8)
	shanghai = shanghai.strftime(shanghai_format)
	return shanghai


def localtime_str(str_format):
	now = datetime.datetime.now()
	return now.strftime(str_format)
