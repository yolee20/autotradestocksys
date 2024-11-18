import tushare as ts
import pandas as pd
import time
import os
import gc  # 导入垃圾回收模块

# 记录开始时间，用于计算耗时
start_time = time.time()

# 设置Tushare的token，替换成你自己在Tushare官网注册获取的真实token
ts.set_token('24acf9bdb6142fa6e47b83a4a5967b2aa85b575f872fa7628e963392')
pro = ts.pro_api()

# 查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# 解析出股票代码列表，作为缓存（简单示例，实际可考虑更高效缓存方式）
stock_code_cache = data['ts_code'].tolist()

# 定义历史日K线数据保存的根文件夹路径
root_save_path = r'D:\program-trade\all_stock_info\history_data'
# 检查保存历史数据的文件夹是否存在，如果不存在则创建
if not os.path.exists(root_save_path):
    os.makedirs(root_save_path)

# 记录开始下载股票历史数据的提示信息
print(f"共获取到 {len(stock_code_cache)} 只股票代码，开始下载历史日K线数据...")

# 遍历股票代码列表，依次下载每只股票的历史日K线数据并保存
for index, ts_code in enumerate(stock_code_cache):
    try:
        # 获取单只股票的历史日K线数据，这里设置了一定的时间范围，可根据需求调整
        stock_data = pro.daily(ts_code=ts_code, start_date='19900101', end_date='20241118')
        if not stock_data.empty:
            # 定义每只股票数据保存的具体文件路径，文件名使用股票代码
            file_path = os.path.join(root_save_path, f"{ts_code}.csv")
            # 使用to_csv方法保存数据，设置chunksize分块处理，每块处理完可视为一个进度阶段
            chunksize = 1000  # 可根据数据量大小调整分块大小
            total_chunks = len(stock_data) // chunksize + (1 if len(stock_data) % chunksize > 0 else 0)
            print(f"开始保存股票 {ts_code} 的历史日K线数据，共 {len(stock_data)} 行，分 {total_chunks} 块处理...")
            for i in range(0, len(stock_data), chunksize):
                chunk = stock_data.iloc[i:i + chunksize]
                if i == 0:  # 若是第一块数据，写入表头
                    chunk.to_csv(file_path, mode='w', encoding='utf-8', index=False)
                else:  # 后续块数据，追加写入文件
                    chunk.to_csv(file_path, mode='a', encoding='utf-8', index=False, header=False)
                progress = (i + chunksize) / len(stock_data) * 100
                print(f"已保存 {i + chunksize} 行，保存进度: {progress:.2f}%")
            print(f"股票 {ts_code} 的历史日K线数据已成功保存至 {file_path}")
        else:
            print(f"股票 {ts_code} 无对应历史日K线数据，跳过保存")
    except ts.RequestError as e:
        print(f"请求获取股票 {ts_code} 的历史日K线数据时出错，错误信息: {e}，将尝试重新获取...")
    except OSError as e:
        print(f"保存股票 {ts_code} 的历史日K线数据时文件操作出错，错误信息: {e}")
    except Exception as e:
        print(f"获取或保存股票 {ts_code} 的历史日K线数据时出现未知错误，错误信息: {e}")
    # 每下载完10只股票显示一次整体下载进度（可根据实际情况调整频率）
    if (index + 1) % 10 == 0:
        overall_progress = (index + 1) / len(stock_code_cache) * 100
        print(f"已下载 {index + 1} 只股票的历史日K线数据，整体下载进度: {overall_progress:.2f}%")
    # 每处理完50只股票触发一次垃圾回收，可根据实际情况调整频率
    if (index + 1) % 50 == 0:
        gc.collect()

# 记录结束时间，计算耗时并输出
end_time = time.time()
elapsed_time = end_time - start_time
print(f"下载并保存所有股票历史日K线数据耗时: {elapsed_time:.2f} 秒")