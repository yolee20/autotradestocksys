---- 创建名为stock_history_k_data的表，用于存储股票历史日K线数据
--CREATE table IF NOT EXISTS stock_history_k_data (
--    -- uuid字段，使用UUID()函数自动生成全局唯一标识符，类型为VARCHAR，长度为36个字符
--    uuid VARCHAR(36) NOT NULL,
--    -- 股票代码字段，类型为VARCHAR，长度为20个字符，用于关联对应的股票基本信息表中的股票，确保数据一致性，且作为关键标识之一
--    ts_code VARCHAR(20) NOT NULL,
--    -- 交易日期字段，类型为DATE，用于记录具体的交易日时间，是K线数据的关键时间维度，与股票代码共同唯一确定一条K线记录
--    trade_date DATE NOT NULL,
--    -- 开盘价字段，类型为DECIMAL，精度为10位，小数点后保留2位，用于存储股票开盘时的价格
--    open_price DECIMAL(10, 2),
--    -- 最高价字段，类型为DECIMAL，精度为10位，小数点后保留2位，记录股票在该交易日内达到的最高价格
--    high_price DECIMAL(10, 2),
--    -- 最低价字段，类型为DECIMAL，精度为10位，小数点后保留2位，记录股票在该交易日内达到的最低价格
--    low_price DECIMAL(10, 2),
--    -- 收盘价字段，类型为DECIMAL，精度为10位，小数点后保留2位，存储股票在该交易日结束时的价格
--    close_price DECIMAL(10, 2),
--    -- 前收盘价字段，类型为DECIMAL，精度为10位，小数点后保留2位，用于对比计算当日股价涨跌情况，即前一个交易日的收盘价
--    pre_close_price DECIMAL(10, 2),
--    -- 涨跌额字段，类型为DECIMAL，精度为10位，小数点后保留2位，记录当日收盘价与前收盘价的差值，体现股价的绝对变化量
--    change_amount DECIMAL(10, 2),
--    -- 涨跌幅字段，类型为DECIMAL，精度为10位，小数点后保留2位，以百分比形式体现股价相对前收盘价的变化幅度
--    pct_change DECIMAL(10, 2),
--    -- 成交量字段，类型为BIGINT，用于存储该交易日股票的成交数量
--    volume BIGINT,
--    -- 成交额字段，类型为DECIMAL，精度为10位，小数点后保留2位，记录该交易日股票的成交金额
--    amount DECIMAL(10, 2),
--    -- 数据来源字段，类型为VARCHAR，长度可根据实际数据源名称长度设定，用于记录该条数据是从哪里获取的，比如来自Tushare
--    data_source VARCHAR(50),
--    -- 数据插入时间字段，类型为DATETIME，记录这条数据插入到数据库的具体时间，方便后续数据管理和追溯
--    insert_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--    -- 将uuid字段设置为主键，确保每条记录的唯一性，方便数据的准确管理和查询
--    PRIMARY KEY (uuid),
--    -- 为ts_code和trade_date两个字段组合添加唯一索引，因为这两个字段联合起来能唯一确定一条K线数据记录
--    -- 同时添加此索引也有助于提高基于股票代码和交易日期进行查询操作时的数据库性能
--    UNIQUE KEY (ts_code, trade_date)
--) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

---- 创建一个BEFORE INSERT触发器，用于在插入数据前自动为uuid字段赋值，和之前的原理一样哒，亲爱的
--DELIMITER //
--CREATE TRIGGER generate_uuid_before_insert_2024
--BEFORE INSERT ON stock_history_k_data_2024
--FOR EACH ROW
--BEGIN
--    SET NEW.uuid = UUID();
--END //
--DELIMITER ;




