from datetime import datetime
import pytz

# 假设这个数字是表示到微秒的时间戳
timestamp_microseconds = 1731778836387
# 将微秒时间戳转换为秒（因为Python的fromtimestamp方法一般处理以秒为单位的时间戳）
timestamp_seconds = timestamp_microseconds / 1000000.0

# 使用fromtimestamp方法将时间戳转换为对应的datetime对象（基于本地时区）
dt_object_local = datetime.fromtimestamp(timestamp_seconds)
print("基于本地时区的时间输出：", dt_object_local.strftime('%Y-%m-%d %H:%M:%S'))

# 转换为指定时区（这里以北京时间，即东八区为例）
beijing_tz = pytz.timezone('Asia/Shanghai')
dt_object_beijing = datetime.fromtimestamp(timestamp_seconds, tz=beijing_tz)
print("转换为北京时间（东八区）的时间输出：", dt_object_beijing.strftime('%Y-%m-%d %H:%M:%S'))