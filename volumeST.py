import tushare as ts
import pandas as pd

# 设置 tushare 的 token，需要你自己在 tushare 官网注册获取
ts.set_token('your_tushare_token')
pro = ts.pro_api()

def get_stock_trading_data(ts_code, start_date, end_date):
    """
    获取指定股票在指定日期范围内的交易数据
    :param ts_code: 股票代码
    :param start_date: 开始日期，格式：YYYYMMDD
    :param end_date: 结束日期，格式：YYYYMMDD
    :return: 交易数据 DataFrame
    """
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
    return df

def classify_trades(df):
    """
    简单示例：根据成交量大小区分主力和散户交易
    这里假设成交量大于均值的为主力交易，小于均值的为散户交易
    :param df: 交易数据 DataFrame
    :return: 主力和散户的买入和卖出量
    """
    volume_mean = df['vol'].mean()
    main_buy_volume = df[df['vol'] > volume_mean]['vol'].sum()
    retail_buy_volume = df[df['vol'] <= volume_mean]['vol'].sum()
    return main_buy_volume, retail_buy_volume

def monitor_stock(ts_code, start_date, end_date):
    """
    监控指定股票在指定日期范围内主力和散户的买入和卖出量
    :param ts_code: 股票代码
    :param start_date: 开始日期，格式：YYYYMMDD
    :param end_date: 结束日期，格式：YYYYMMDD
    """
    data = get_stock_trading_data(ts_code, start_date, end_date)
    if not data.empty:
        main_volume, retail_volume = classify_trades(data)
        print(f"股票代码: {ts_code}")
        print(f"主力买入量: {main_volume}")
        print(f"散户买入量: {retail_volume}")
    else:
        print(f"未获取到 {ts_code} 在 {start_date} 到 {end_date} 的交易数据。")

if __name__ == "__main__":
    # 示例股票代码
    stock_code = '000001.SZ'
    start_date = '20240101'
    end_date = '20241231'
    monitor_stock(stock_code, start_date, end_date)
