import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import baostock as bs
from statsmodels.api import qqplot

os.chdir(os.getcwd())
plt.rcParams['font.sans-serif'] = ['SimHei']  # 处理中文显示问题
warnings.filterwarnings("ignore")  # 不再显示warning


def getIndexDate(code: str, start_date: str, end_date: str):
    lg = bs.login()
    # 获取指数(综合指数、规模指数、一级行业指数、二级行业指数、策略指数、成长指数、价值指数、主题指数)K线数据
    # 综合指数，例如：sh.000001 上证指数，sz.399106 深证综指 等；
    # 规模指数，例如：sh.000016 上证50，sh.000300 沪深300，sh.000905 中证500，sz.399001 深证成指等；
    # 一级行业指数，例如：sh.000037 上证医药，sz.399433 国证交运 等；
    # 二级行业指数，例如：sh.000952 300地产，sz.399951 300银行 等；
    # 策略指数，例如：sh.000050 50等权，sh.000982 500等权 等；
    # 成长指数，例如：sz.399376 小盘成长 等；
    # 价值指数，例如：sh.000029 180价值 等；
    # 主题指数，例如：sh.000015 红利指数，sh.000063 上证周期 等；

    # 详细指标参数，参见“历史行情指标参数”章节；“周月线”参数与“日线”参数不同。
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(code,
                                      "Date,code,open,high,low,Close,volume",
                                      start_date, end_date, frequency="d")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv("%s.csv" % (code.replace(".", "_")), index=False)
    bs.logout()


getIndexDate(code='sz.399106', start_date='2014-01-01', end_date='2014-12-01')

def TrainResults():

    ChinaBank = pd.read_csv('sz_399106.csv', index_col='Date', parse_dates=['Date'])
    ChinaBank.index = pd.to_datetime(ChinaBank.index)
    sub = ChinaBank['2014-01':'2014-06']['Close']
    train = sub.loc['2014-01':'2014-03']
    test = sub.loc['2014-04':'2014-06']

    # 获取AIC,BIC
    train_results = sm.tsa.arma_order_select_ic(
        train, ic=['aic', 'bic'], trend='nc', max_ar=4, max_ma=4)
    print('AIC', train_results.aic_min_order)
    print('BIC', train_results.bic_min_order)

    # 模型检验
    model = sm.tsa.ARIMA(train, order=(1, 0, 0))
    results = model.fit()
    resid = results.resid #赋值
    fig = plt.figure(figsize=(12,8))
    fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40)
    # plt.show()


    resid = results.resid#残差
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    fig = qqplot(resid, line='q', ax=ax, fit=True)

    model = sm.tsa.ARIMA(sub, order=(1, 0, 0))
    results = model.fit()
    predict_sunspots = results.predict(start=str('2014-04'),end=str('2014-05'),dynamic=False)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = sub.plot(ax=ax)
    predict_sunspots.plot(ax=ax)
    plt.show()
TrainResults()