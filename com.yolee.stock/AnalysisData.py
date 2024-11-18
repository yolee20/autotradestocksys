import requests
import json
import pymysql
from tqdm import tqdm

# 请求的URL
url = "https://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid=1.600839&klt=101&fqt=1&cb=jsonp1731780512941"

# 发送请求获取数据
try:
    response = requests.get(url)
    if response.status_code == 200:
        # 处理JSONP格式数据，提取真正的JSON字符串内容
        content_text = response.text
        json_str = content_text[content_text.find("(") + 1: -2]
        data = json.loads(json_str)

        # 分析数据字段含义（以下为推测，具体以接口文档为准）
        if 'rc' in data and data['rc'] == 0:
            if 'data' in data:
                data_content = data['data']
                print("以下是对各字段含义的分析：")
                print("股票代码（code）：用于唯一标识一只股票，是在证券市场中区分不同股票的重要编号，不同股票有其特定且唯一的代码。")
                print("市场代码（market）：可能用于区分不同的交易市场，例如不同的证券交易所等，便于对股票所属市场进行归类管理。")
                print("股票名称（name）：直观展示股票所对应的公司名称或者产品名称等，方便投资者识别和区分不同股票。")
                print("小数位数（xsws）：代表价格等数据在记录时保留的小数位数，用于精确表示股票价格、成交量等数值信息的精度。")
                print("总交易天数（dktotal）：统计该股票从上市以来或者特定统计周期内总的交易天数情况，可用于分析股票交易活跃度等方面。")
                print("前收盘价（preKPrice）：指的是上一个交易日结束时该股票的收盘价格，常作为衡量下一个交易日股价涨跌的重要参考基准。")
                print("K线数据（klines列表中每个元素拆分后的各字段）：")
                print("  日期（对应列表元素拆分后的第1个字段）：代表该条K线数据对应的具体交易日期，格式通常为年-月-日，明确了交易发生的时间点。")
                print("  开盘价（对应列表元素拆分后的第2个字段）：是指在当天交易日开始时，股票首次成交的价格，反映了市场对该股票在当日起始阶段的估值情况。")
                print("  最高价（对应列表元素拆分后的第3个字段）：在当日整个交易过程中，股票所达到的最高成交价格，体现股价在当日的上涨上限情况。")
                print("  最低价（对应列表元素拆分后的第4个字段）：在当日整个交易过程中，股票所达到的最低成交价格，展示股价在当日的下跌下限情况。")
                print("  收盘价（对应列表元素拆分后的第5个字段）：在当天交易日结束时，股票最后一笔成交的价格，往往是当日交易情况的一个重要总结性价格指标。")
                print("  成交量（对应列表元素拆分后的第6个字段）：记录了当日该股票成交的总数量，单位通常根据证券市场规定，是衡量股票交易活跃度以及市场供需关系的重要指标之一。")
                print("  成交额（对应列表元素拆分后的第7个字段）：表示当日该股票成交的总金额，是通过成交量与成交价格等因素计算得出，综合反映了股票当日的交易规模。")
                print("  振幅（对应列表元素拆分后的第8个字段）：用于衡量股价在当日交易过程中的波动幅度，计算公式一般是（最高价 - 最低价）/ 前收盘价，能直观体现股价的当日波动剧烈程度。")
                print("  涨跌幅（对应列表元素拆分后的第9个字段）：体现股价相对于前一交易日收盘价的涨跌百分比情况，计算公式大致为（收盘价 - 前收盘价）/ 前收盘价 * 100%，是投资者关注的重要涨跌指标。")
                print("  涨跌额（对应列表元素拆分后的第10个字段）：指的是股价相对于前一交易日收盘价的涨跌具体金额差值，即收盘价减去前收盘价，直观展示股价的涨跌数值变化。")
                print("  换手率（对应列表元素拆分后的第11个字段）：反映了股票在一定时间内的流通转手情况，通常是用成交量与流通股本的比值来计算，是衡量股票流通性以及市场活跃度的关键指标之一。")

                # MySQL数据库连接配置，根据实际情况修改
                config = {
                    'host': 'localhost',
                    'user': 'root',
                    'password': 'root'
                }
                # 连接到MySQL服务器
                conn = pymysql.connect(**config)
                cursor = conn.cursor()

                # 创建名为eastmoney的数据库（如果不存在的话），指定utf8字符编码
                create_database_sql = "CREATE DATABASE IF NOT EXISTS eastmoney CHARACTER SET utf8mb4"
                cursor.execute(create_database_sql)
                # 使用刚创建的数据库
                cursor.execute("USE eastmoney")

                # 创建stock_info表（如果不存在）及字段说明，将decimal字段名改为xsws，指定utf8字符编码
                create_stock_info_table_sql = """
                CREATE TABLE IF NOT EXISTS stock_info (
                    id INT AUTO_INCREMENT PRIMARY KEY,  -- 自增主键，用于唯一标识每一条股票基本信息记录
                    code VARCHAR(10) NOT NULL,  -- 股票代码，长度设为10，存储如600839这样的代码，不允许为空
                    market INT,  -- 市场代码，存储表示市场的整数标识
                    name VARCHAR(50),  -- 股票名称，长度设为50，可存储常见的股票全称等
                    xsws INT,  -- 小数位数，记录价格等数据保留的小数位数量，字段名改为xsws
                    dktotal INT,  -- 总交易天数，统计股票总的交易天数
                    preKPrice DECIMAL(10, 2)  -- 前收盘价，用 decimal 类型存储，共10位，其中小数部分2位，精确表示价格
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
                cursor.execute(create_stock_info_table_sql)

                # 创建stock_history表（如果不存在）及字段说明，指定utf8字符编码，将open字段名改为openPrice，并为today字段建索引
                create_stock_history_table_sql = """
                CREATE TABLE IF NOT EXISTS stock_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,  -- 自增主键，用于唯一标识每一条股票历史数据记录
                    stock_info_id INT NOT NULL,  -- 外键，关联stock_info表的id字段，确定该历史数据属于哪只股票，不允许为空
                    today DATE,  -- 交易日期，存储如年-月-日格式的日期数据
                    openPrice DECIMAL(10, 2),  -- 开盘价，字段名改为openPrice，用 decimal 类型存储，共10位，其中小数部分2位，精确表示价格
                    high DECIMAL(10, 2),  -- 最高价，用 decimal 类型存储，共10位，其中小数部分2位，精确表示价格
                    low DECIMAL(10, 2),  -- 最低价，用 decimal 类型存储，共10位，其中小数部分2位，精确表示价格
                    close DECIMAL(10, 2),  -- 收盘价，用 decimal 型存储，共10位，其中小数部分2位，精确表示价格
                    volume BIGINT,  -- 成交量，用大整数类型存储，因为成交量数值通常较大
                    amount DECIMAL(20, 2),  -- 成交额，用 decimal 类型存储，共20位，其中小数部分2位，能适应较大金额数值
                    amplitude DECIMAL(10, 2),  -- 振幅，用 decimal 类型存储，共10位，其中小数部分2位，精确表示波动幅度
                    change_percentage DECIMAL(10, 2),  -- 涨跌幅，用 decimal 类型存储，共10位，其中小数部分2位，精确表示涨跌百分比
                    change_amount DECIMAL(10, 2),  -- 涨跌额，用 decimal 类型存储，共10位，其中小数部分2位，精确表示涨跌金额差值
                    turnover DECIMAL(10, 2),  -- 换手率，用 decimal 类型存储，共10位，其中小数部分2位，精确表示换手率数值
                    FOREIGN KEY (stock_info_id) REFERENCES stock_info(id)  -- 外键约束，建立与stock_info表的关联关系，确保数据一致性
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
                cursor.execute(create_stock_history_table_sql)

                # 提取股票基本信息并插入stock_info表，注意使用新的字段名xsws
                stock_info_data = (
                    data_content['code'],
                    data_content['market'],
                    data_content['name'],
                    data_content['decimal'],
                    data_content['dktotal'],
                    data_content['preKPrice']
                )
                insert_stock_info_sql = "INSERT INTO stock_info (code, market, name, xsws, dktotal, preKPrice) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_stock_info_sql, stock_info_data)
                conn.commit()
                stock_info_id = cursor.lastrowid

                # 提取历史数据并插入stock_history表，使用tqdm显示进度，注意使用新的字段名openPrice
                total_records = len(data_content['klines'])
                with tqdm(total=total_records, desc="保存历史数据进度") as pbar:
                    for kline in data_content['klines']:
                        fields = kline.split(',')
                        stock_history_data = (
                            stock_info_id,
                            fields[0],
                            float(fields[1]),
                            float(fields[2]),
                            float(fields[3]),
                            float(fields[4]),
                            int(fields[5]),
                            float(fields[6]),
                            float(fields[7]),
                            float(fields[8]),
                            float(fields[9]),
                            float(fields[10])
                        )
                        insert_stock_history_sql = """
                        INSERT INTO stock_history (stock_info_id, today, openPrice, high, low, close, volume, amount, amplitude, change_percentage, change_amount, turnover) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_stock_history_sql, stock_history_data)
                        conn.commit()
                        pbar.update(1)

                print("数据已成功保存到MySQL数据库对应的表中。")
                cursor.close()
                conn.close()
            else:
                print("返回数据中没有'data'字段，无法进一步处理和保存数据。")
        else:
            print("请求失败，错误码:", data['rc'])
    else:
        print(f"请求失败，状态码: {response.status_code}")
except requests.RequestException as e:
    print(f"请求发生异常: {e}")
except pymysql.Error as e:
    print(f"数据库操作出现异常: {e}")