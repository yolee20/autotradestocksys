

import tushare as ts
import pandas as pd
import time
import os

# 记录开始时间，用于计算耗时
start_time = time.time()

# 设置Tushare的token，替换成你自己在Tushare官网注册获取的真实token
ts.set_token('24acf9bdb6142fa6e47b83a4a5967b2aa85b575f872fa7628e963392')
pro = ts.pro_api()

# 查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# 定义保存文件的路径及文件名，修改为all_stock_list.csv
file_path = r'D:\program-trade\all_stock_info\all_stock_list.csv'

# 检查文件是否存在，如果不存在则创建所在文件夹（如果文件夹也不存在的话）
if not os.path.exists(file_path):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# 获取数据的总行数，用于显示保存进度
total_rows = len(data)
print(f"数据总行数为: {total_rows} 行，开始保存数据...")

# 逐行写入文件来模拟保存进度显示（实际可以使用更高效的方式，这里主要为展示进度效果）
with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(','.join(data.columns) + '\n')  # 先写入表头
    for index, row in enumerate(data.values):
        f.write(','.join(map(str, row)) + '\n')
        # 每写入100行显示一次保存进度（可根据实际情况调整显示频率）
        if (index + 1) % 100 == 0:
            progress = (index + 1) / total_rows * 100
            print(f"已保存 {index + 1} 行，保存进度: {progress:.2f}%")

print(f"数据已成功保存至 {file_path}")

# 记录结束时间，计算耗时并输出
end_time = time.time()
elapsed_time = end_time - start_time
print(f"保存数据耗时: {elapsed_time:.2f} 秒")

