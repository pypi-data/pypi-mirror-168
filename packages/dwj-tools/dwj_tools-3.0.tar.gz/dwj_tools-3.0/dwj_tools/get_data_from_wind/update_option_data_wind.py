#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   update_option_data_wind.py
@Time    :   2022/01/13 16:15:19
@Author  :   DingWenjie
@Contact :   359582058@qq.com
@Desc    :   update data from Wind
'''

import os
from WindPy import w
from dwj_tools.Lib_OptionCalculator import CalDeltaCall
from dwj_tools.Lib_OptionCalculator import CalIVCall
from dwj_tools.Lib_OptionCalculator import CalDeltaPut
from dwj_tools.Lib_OptionCalculator import CalIVPut
from dwj_tools.Lib_OptionCalculator import CalGammaCall
from dwj_tools.Lib_OptionCalculator import CalGammaPut
from dwj_tools.Lib_OptionCalculator import CalVegaCall
from dwj_tools.Lib_OptionCalculator import CalVegaPut
from dwj_tools.Lib_OptionCalculator import CalVannaCallPct
from dwj_tools.Lib_OptionCalculator import CalVannaPutPct
import warnings
import numpy as np
import time
import datetime
import pandas as pd
w.start()
warnings.simplefilter('ignore')

pt = os.path.dirname(os.path.realpath(__file__))
files = {
        'A': os.path.join(pt, 'option_50_data_wind.h5'),
        'B': os.path.join(pt, 'tradingday.xlsx'),
        'C': os.path.join(pt, 'etf_50_data_wind.h5')
}
def update():
    start = time.perf_counter()
    # df_50 = pd.read_hdf(r'option_50_data_wind.h5')
    # tradingday = pd.read_excel('tradingday.xlsx')
    df_50 = pd.read_hdf(files['A'])
    tradingday = pd.read_excel(files['B'])
    crtdate = datetime.date.today()
    crtdate = datetime.datetime(crtdate.year, crtdate.month,
                                crtdate.day, 00, 00)
    crtdate_str = crtdate.strftime("%Y-%m-%d")
    idx = tradingday.loc[tradingday.date < crtdate].index.tolist()[-1]
    target_date = tradingday.date[idx]
    target_date_str = target_date.strftime("%Y-%m-%d")
    print(f'今天的日期为{crtdate_str},要更新数据到当前日期的前一个交易日截止!')
    old_date = list(df_50['date'])[-1]
    old_date_str = old_date.strftime("%Y-%m-%d")
    print(f'已有的 excel 中数据截止到{old_date_str}')
    if old_date == target_date:
        print('数据已经是最新!无需更新,已停止程序.')
    else:
        idx_old_date = tradingday.loc[tradingday.date <=
                                    old_date].index.tolist()[-1]
        startdate = tradingday.date[idx_old_date+1].strftime("%Y-%m-%d")
        enddate = target_date.strftime("%Y-%m-%d")
        print('*'*20 + '开始更新数据' + '*'*20)
        print('开始更新 etf50 数据')
        _, new_etf = w.wsd("510050.SH", "close,open,high,low,volume",
                        '2015-01-12', enddate, usedf=True)
        print('etf50 数据更新完毕\n' + '-'*45 + '\n' + '开始更新期权数据')
        _, df = w.wset("optiondailyquotationstastics",
                    f"startdate={startdate};enddate={enddate};exchange=sse;windcode=510050.SH", usedf=True)
        df = df.iloc[::-1]
        df.drop(['delta', 'gamma', 'vega', 'theta', 'rho'], axis=1, inplace=True)
        code = list(df['option_code'])
        code = [str(x)+'.SH' for x in code]
        df['option_code'] = code
        print('获取原始数据成功!开始进行计算')
        r = np.log(1.018)
        df.index = df['date']
        date = df.index.drop_duplicates(keep='first')
        df1 = pd.DataFrame()
        l = len(date)
        Tau = []
        Maturity = []
        exe_ratio = []
        delta = []
        iv = []
        gamma = []
        vega = []
        vanna = []
        flag = []
        print('开始添加到期月份,剩余存续日,合约乘数信息')
        for i,Temp_date in enumerate(date):
            temp_df = df.loc[(df.index == Temp_date)]
            temp_code = list(temp_df['option_code'])
            strr = ','
            temp_code = strr.join(temp_code)
            temp_date = Temp_date.strftime("%Y-%m-%d")
            temp_m = w.wsd(temp_code, "lasttradingdate",
                        temp_date, temp_date).Data[0]
            temp_m = [x.strftime("%Y%m") for x in temp_m]
            Maturity = Maturity + temp_m
            Tau = Tau + w.wsd(temp_code, "ptmtradeday",
                            temp_date, temp_date).Data[0]
            exe_ratio = exe_ratio + \
                w.wsd(temp_code, "exe_ratio", temp_date, temp_date).Data[0]
        df['maturity'] = Maturity
        df['tau'] = Tau
        df['exe_ratio'] = exe_ratio
        print('添加 maturity/tau/exeratio 完毕!')
        for j in range(l):
            crt_date = date[j]
            print(f'computing Greeks:{crt_date}')
            true_option_all = df.loc[(df.index == crt_date)].sort_values(
                by='exerciseprice')
            maturity = true_option_all['maturity']\
                .drop_duplicates(keep='first').tolist()
            maturity.sort()
            for i in range(4):
                true_option = true_option_all\
                    .loc[list(true_option_all['maturity'] == maturity[i]), :]
                crt_bool = ['购' in true_option['option_name'][i]
                            for i in range(len(true_option))]
                true_option_call = true_option[crt_bool]
                crt_bool_put = ['沽' in true_option['option_name'][i]
                                for i in range(len(true_option))]
                true_option_put = true_option[crt_bool_put]
                if df1.empty:
                    df1 = true_option_call.append(true_option_put)
                else:
                    df1 = df1.append(true_option_call).append(true_option_put)
                K = [float(i) for i in np.array(true_option_call['exerciseprice'])]
                K = np.array(K)
                try:
                    tau = int(true_option.tau.iloc[0])/244
                except IndexError:
                    print('Error:wrong tau')
                iiidd = np.abs(np.array(true_option_call['close'])
                            - np.array(true_option_put['close'])).argmin()
                stock_price = (np.array(true_option_call['close'])
                            + K*np.exp(-tau*r)
                            - np.array(true_option_put['close']))[iiidd]
                for k in range(len(true_option_call)):
                    temp_code = true_option_call['option_code'][k]
                    temp_date = true_option_call['date'][k].strftime("%Y-%m-%d")
                    implied_vol = CalIVCall(
                        S=stock_price, K=K[k], T=tau, r=r, c=true_option_call['close'].iloc[k])
                    iv = iv + [implied_vol]
                    delta = delta + \
                        [CalDeltaCall(S=stock_price, K=K[k],
                                    T=tau, r=r, iv=implied_vol)]
                    gamma = gamma + \
                        [CalGammaCall(S=stock_price, K=K[k],
                                    T=tau, r=r, iv=implied_vol)]
                    vega = vega + \
                        [CalVegaCall(S=stock_price, K=K[k],
                                    T=tau, r=r, iv=implied_vol)]
                    vanna = vanna + \
                        [CalVannaCallPct(S=stock_price, K=K[k],
                                        T=tau, r=r, iv=implied_vol)]
                    flag = flag + ['C']
                for k in range(len(true_option_put)):
                    temp_code = true_option_put['option_code'][k]
                    temp_date = true_option_put['date'][k].strftime("%Y-%m-%d")
                    implied_vol = CalIVPut(
                        S=stock_price, K=K[k], T=tau, r=r, p=true_option_put['close'].iloc[k])
                    iv = iv + [implied_vol]
                    delta = delta + \
                        [CalDeltaPut(S=stock_price, K=K[k],
                                    T=tau, r=r, iv=implied_vol)]
                    gamma = gamma + \
                        [CalGammaPut(S=stock_price, K=K[k],
                                    T=tau, r=r, iv=implied_vol)]
                    vega = vega + \
                        [CalVegaPut(S=stock_price, K=K[k],
                                    T=tau, r=r, iv=implied_vol)]
                    vanna = vanna + \
                        [CalVannaPutPct(S=stock_price, K=K[k],
                                        T=tau, r=r, iv=implied_vol)]
                    flag = flag + ['P']
        print('恭喜,计算完毕!')
        df1['date.1'] = df1['date']
        df1['iv'] = iv
        df1['delta'] = delta
        df1['gamma'] = gamma
        df1['vega'] = vega
        df1['vanna'] = vanna
        df1['flag'] = flag
        end = time.perf_counter()
        spend = end-start
        print(f'更新数据共耗时{spend}')
        df_final = df_50.append(df1)
        df_final.index = df_final['date']
        df_final.drop(['date.1'],axis=1,inplace=True)
        print('开始保存数据')
        new_etf.to_hdf(files['C'],key='etf_50')
        df_final.to_hdf(files['A'],key='option_50')
        print('保存成功!')

if __name__ == '__main__':
    update()