import datetime
import time



def send_otp_code(phone_number, code):
    pass


def cal_seconds(value):
    x = time.strptime(value.split(',')[0],'%H:%M:%S.%f')
    result = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

    return result