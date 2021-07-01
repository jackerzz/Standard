import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader
import os
os.chdir(os.getcwd())
plt.rcParams['font.sans-serif'] = ['SimHei']  # 处理中文显示问题


def getIndexDate(code: str, start_date: str, end_date: str):
    # 登陆系统
    bs.login()
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
                                      "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                                      start_date, end_date, frequency="d")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv("%s.csv" % (code.replace(".", "_")), index=False)
    bs.logout()
    return


def generate_df_affect_by_n_days(series, n, index=False):
    if len(series) <= n:
        raise Exception(
            "The Length of series is %d, while affect by (n=%d)." % (len(series), n))
    df = pd.DataFrame()
    for i in range(n):
        df['c%d' % i] = series.tolist()[i:-(n - i)]
    df['y'] = series.tolist()[n:]
    if index:
        df.index = series.index[n:]
    return df


def readData(code: str, column='high', n=30, all_too=True, index=False, train_end=-300):
    df = pd.read_csv(code.replace(".", "_")+".csv", index_col=0)
    df.index = list(
        map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"), df.index))
    df_column = df[column].copy()
    df_column_train, df_column_test = df_column[:
                                                train_end], df_column[train_end - n:]
    df_generate_from_df_column_train = generate_df_affect_by_n_days(
        df_column_train, n, index=index)
    if all_too:
        return df_generate_from_df_column_train, df_column, df.index.tolist()
    return df_generate_from_df_column_train


class RNN(nn.Module):
    '''
        网络搭建
    '''

    def __init__(self, input_size):
        super(RNN, self).__init__()
        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=64,
            num_layers=1,
            batch_first=True
        )
        self.out = nn.Sequential(
            nn.Linear(64, 1)
        )

    def forward(self, x):
        # None 表示 hidden state 会用全0的 state
        r_out, (h_n, h_c) = self.rnn(x, None)
        out = self.out(r_out)
        return out


class TrainSet(Dataset):
    def __init__(self, data):
        # 定义好 data 的路径
        self.data, self.label = data[:, :-1].float(), data[:, -1].float()

    def __getitem__(self, index):
        return self.data[index], self.label[index]

    def __len__(self):
        return len(self.data)


def trainModel(saveModelName: str, n: int, LR: float, EPOCH: int, trainloader: pd.DataFrame):
    '''
        训练模型
            - saveModelName: 保存的模型名称
            - n: 对于nn.LSTM 中 input_size
            - LR:模型的学习率
            - EPOCH:执行批次
            - trainloader:训练数据集
    '''
    rnn = RNN(n)
    # 优化所有CNN参数
    optimizer = torch.optim.Adam(rnn.parameters(), lr=LR)
    loss_func = nn.MSELoss()

    for step in range(EPOCH):
        for tx, ty in trainloader:
            output = rnn(torch.unsqueeze(tx, dim=0))
            loss = loss_func(torch.squeeze(output), ty)
            optimizer.zero_grad()  # 清除此培训步骤的渐变
            loss.backward()  # 反向传播，计算梯度
            optimizer.step()
        print(step, loss)
        if step % 10:
            torch.save(rnn, saveModelName)
    torch.save(rnn, saveModelName)
    return rnn


def TrainRun(code, start_date, end_date):
    n = 30
    LR = 0.0001
    EPOCH = 100
    train_end = -500

    getIndexDate(code, start_date, end_date)
    # 数据集建立
    df, df_all, df_index = readData(code, 'high', n=n, train_end=train_end)

    df_all = np.array(df_all.tolist())
    plt.plot(df_index, df_all, label='real-data')

    df_numpy = np.array(df)

    df_numpy_mean = np.mean(df_numpy)
    df_numpy_std = np.std(df_numpy)

    df_numpy = (df_numpy - df_numpy_mean) / df_numpy_std

    # 检查该股票是否存在模型
    modename = code+'.pkl'
    if os.path.exists(modename):
        rnn = torch.load(modename)
    else:
        df_tensor = torch.Tensor(df_numpy)
        trainset = TrainSet(df_tensor)
        trainloader = DataLoader(trainset, batch_size=10, shuffle=True)
        rnn = trainModel(modename, n, LR, EPOCH, trainloader)

    # 获取训练数据及测试数据
    generate_data_train = []
    generate_data_test = []
    test_index = len(df_all) + train_end
    df_all_normal = (df_all - df_numpy_mean) / df_numpy_std
    df_all_normal_tensor = torch.Tensor(df_all_normal)
    for i in range(n, len(df_all)):
        x = df_all_normal_tensor[i - n:i]
        x = torch.unsqueeze(torch.unsqueeze(x, dim=0), dim=0)
        y = rnn(x)
        if i < test_index:
            generate_data_train.append(torch.squeeze(
                y).detach().numpy() * df_numpy_std + df_numpy_mean)
        else:
            generate_data_test.append(torch.squeeze(
                y).detach().numpy() * df_numpy_std + df_numpy_mean)

    plt.plot(df_index[n:train_end], generate_data_train,
             label='generate_train')
    plt.plot(df_index[train_end:], generate_data_test, label='generate_test')
    plt.legend()
    plt.show()

    plt.cla()
    plt.plot(df_index[train_end:-400],
             df_all[train_end:-400], label='real-data')
    plt.plot(df_index[train_end:-400],
             generate_data_test[:-400], label='generate_test')
    plt.legend()
    plt.show()


TrainRun(
    code="sz.399376",
    start_date='2018-01-01',
    end_date='2021-06-10',
)
