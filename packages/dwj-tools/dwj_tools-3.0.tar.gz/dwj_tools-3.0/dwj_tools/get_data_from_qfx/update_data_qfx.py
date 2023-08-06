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
import tcoreapi_mq as t
import time
import datetime
import pandas as pd
import os
#core = t.TCoreZMQ(quote_port="51630", trade_port="51600")
core = t.TCoreZMQ(quote_port="51864", trade_port="51834")
warnings.simplefilter('ignore')

pt = os.path.dirname(os.path.realpath(__file__))
files = {
        'A': os.path.join(pt, 'option_data_50.h5'),
        'B': os.path.join(pt, 'tradingday.xlsx'),
        'C': os.path.join(pt, 'etf_50.h5'),
        'D': os.path.join(pt, 'etf_300.h5'),
        'E': os.path.join(pt, 'option_data_300.h5'),
}
def update():
    start_time = time.perf_counter()
    df_50_old = pd.read_hdf(files['A'])
    df_300_old = pd.read_hdf(files['E'])
    tradingday = pd.read_excel(files['B'])
    etf_50 = pd.read_hdf(files['C'])
    etf_300 = pd.read_hdf(files['D'])
    crtdate = datetime.date.today()
    crtdate = datetime.datetime(crtdate.year, crtdate.month,
                                crtdate.day, 00, 00)
    crtdate_str = crtdate.strftime("%Y%m%d")
    idx = tradingday.loc[tradingday.date < crtdate].index.tolist()[-1]
    target_date = tradingday.date[idx]
    # target_date_str = target_date.strftime("%Y-%m-%d")
    print(f'今天的日期为{crtdate_str},要更新数据到当前日期的前一个交易日截止!')
    old_date = list(df_50_old['date'])[-1]
    old_date_str = old_date.strftime("%Y-%m-%d")
    print(f'已有的 excel 中数据截止到{old_date_str}')
    if old_date == target_date:
        print('数据已经是最新!无需更新,已停止程序.')
    else:
        idx_old_date = tradingday.loc[tradingday.date <=
                                    old_date].index.tolist()[-1]
        startdate = tradingday.date[idx_old_date+1].strftime("%Y%m%d")
        enddate = target_date.strftime("%Y%m%d")
        print('*'*20 + '开始更新数据' + '*'*20)
        print('开始更新 etf50 数据')
        etf_50_new = pd.DataFrame(core.SubHistory('TC.S.SSE.510050', 'DK', '2020010200', enddate+'00'))
        etf_300_new = pd.DataFrame(core.SubHistory('TC.S.SSE.510300', 'DK', '2020010200', enddate+'00'))
        # etf_50 = etf_50.append(etf_50_new)
        # etf_300 = etf_300.append(etf_300_new)

        print('etf50 数据更新完毕\n' + '-'*45 + '\n' + '开始更新期权数据')
        log = True
        date = list(tradingday['date'])[idx_old_date+1:idx+1]
        df_50 = pd.DataFrame()
        df_300 = pd.DataFrame()
        for i in range(len(date)):
            crt_date = date[i].strftime('%Y%m%d')
            print(crt_date)
            try:
                a = core.QueryAllInstrumentInfo("Options", crt_date)
                a = pd.DataFrame(a)
            except:
                a = core.QueryAllInstrumentInfo("Options", crt_date)
                a = pd.DataFrame(a)
            b = a['Instruments']['Node']
            c = pd.DataFrame(b[0])
            list50 = c.iloc[0, -1]['Node'][2]['Node']\
                + c.iloc[0, -1]['Node'][3]['Node']\
                + c.iloc[0, -1]['Node'][4]['Node'] + c.iloc[0, -1]['Node'][5]['Node']
            list300 = c.iloc[1, -1]['Node'][2]['Node']\
                + c.iloc[1, -1]['Node'][3]['Node']\
                + c.iloc[1, -1]['Node'][4]['Node'] + c.iloc[1, -1]['Node'][5]['Node']
            for ii in range(4):
                if log:
                    print(ii)
                maturity = list50[2*ii]['ExpirationDate'][0]
                tau = list50[2*ii]['TradeingDays'][0]
                call_50 = list50[2*ii]['Contracts']
                put_50 = list50[2*ii+1]['Contracts']
                call_300 = list300[2*ii]['Contracts']
                put_300 = list300[2*ii+1]['Contracts']
                temp1 = pd.DataFrame()
                temp2 = pd.DataFrame()
                for j in range(len(call_50)):
                    code = call_50[j]
                    start = crt_date+'00'
                    end = crt_date+'98'
                    his = core.SubHistory(code, 'DK', start, end)
                    his = pd.DataFrame(his)
                    his['code'] = code
                    his['maturity'] = maturity
                    his['tau'] = tau
                    d = pd.DataFrame(his, index=[0])
                    temp1 = temp1.append(d)
                if log:
                    print('50call')
                for k in range(len(put_50)):
                    code = put_50[k]
                    start = crt_date+'00'
                    end = crt_date+'98'
                    if log:
                        print(code)
                    his = core.SubHistory(code, 'DK', start, end)
                    his = pd.DataFrame(his)
                    his['code'] = code
                    his['maturity'] = maturity
                    his['tau'] = tau
                    d = pd.DataFrame(his, index=[0])
                    temp1 = temp1.append(d)
                if log:
                    print('50put')
                for m in range(len(call_300)):
                    code = call_300[m]
                    start = crt_date+'00'
                    end = crt_date+'98'
                    his = core.SubHistory(code, 'DK', start, end)
                    his = pd.DataFrame(his)
                    his['code'] = code
                    his['maturity'] = maturity
                    his['tau'] = tau
                    d = pd.DataFrame(his, index=[0])
                    temp2 = temp2.append(d)
                if log:
                    print('300call')
                for n in range(len(put_300)):
                    code = put_300[n]
                    if log:
                        print(code)
                    start = crt_date+'00'
                    end = crt_date+'98'
                    his = core.SubHistory(code, 'DK', start, end)
                    his = pd.DataFrame(his)
                    his['code'] = code
                    his['maturity'] = maturity
                    his['tau'] = tau
                    d = pd.DataFrame(his, index=[0])
                    temp2 = temp2.append(d)
                if log:
                    print('300put')
                df_50 = df_50.append(temp1)
                df_300 = df_300.append(temp2)

        data_300 = df_300.dropna(axis=0, subset=['Date'])
        data_50 = df_50.dropna(axis=0, subset=['Date'])
        data_50.index = range(len(data_50))
        data_300.index = range(len(data_300))
        date50 = [datetime.datetime.strptime(str(data_50['Date'][i]), '%Y%m%d')
                  for i in range(len(data_50))]
        data_50.index = date50
        data_50['date'] = date50
        date300 = [datetime.datetime.strptime(str(int(data_300['Date'][i])), '%Y%m%d')
                    for i in range(len(data_300))]
        data_300.index = date300
        data_300['date'] = date300
        strike = []
        for i in range(len(data_50)):
            cc = data_50['code'][i]
            if len(cc.split('.C.')) > 1:
                strike = strike + [cc.split('.C.')[1]]
            else:
                strike = strike + [cc.split('.P.')[1]]

        data_50['strike'] = strike
        strike = []
        for i in range(len(data_300)):
            cc = data_300['code'][i]
            if len(cc.split('.C.')) > 1:
                strike = strike + [cc.split('.C.')[1]]
            else:
                strike = strike + [cc.split('.P.')[1]]
        data_300['strike'] = strike
        data_300['Close'] = pd.to_numeric(data_300['Close'])
        data_50['Close'] = pd.to_numeric(data_50['Close'])
        data_300['strike'] = pd.to_numeric(data_300['strike'])
        data_50['strike'] = pd.to_numeric(data_50['strike'])
        data_300['tau'] = pd.to_numeric(data_300['tau'])
        data_50['tau'] = pd.to_numeric(data_50['tau'])
        # compute 50
        df1 = pd.DataFrame()
        l = len(date)
        delta = []
        iv = []
        gamma = []
        vega = []
        vanna = []
        r = np.log(1.018)
        for j in range(l):
            crt_date = date[j]
            print(f'computing:{crt_date}')
            true_option_all = data_50.loc[(data_50.index == crt_date)]
            maturity = true_option_all['maturity']\
                .drop_duplicates(keep='first').tolist()
            maturity.sort()
            for i in range(4):
                true_option = true_option_all\
                    .loc[list(true_option_all['maturity'] == maturity[i]), :]
                if df1.empty:
                    df1 = true_option
                else:
                    df1 = df1.append(true_option)
                crt_bool = ['.C.' in true_option['code'][i]
                            for i in range(len(true_option))]
                true_option_call = true_option[crt_bool]
                crt_bool_put = ['.P.' in true_option['code'][i]
                                for i in range(len(true_option))]
                true_option_put = true_option[crt_bool_put]
                K = [float(i) for i in np.array(true_option_call['strike'])]
                K = np.array(K)
                try:
                    tau = int(true_option.tau.iloc[0])/244
                except IndexError:
                    print('Error:wrong tau')
                iiidd = np.abs(np.array(true_option_call['Close'])
                               - np.array(true_option_put['Close'])).argmin()
                stock_price = (np.array(true_option_call['Close'])
                               + K*np.exp(-tau*r)
                               - np.array(true_option_put['Close']))[iiidd]
                for k in range(len(true_option_call)):
                    implied_vol = CalIVCall(
                        S=stock_price, K=K[k], T=tau, r=r, c=true_option_call['Close'].iloc[k])
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
                for k in range(len(true_option_put)):
                    implied_vol = CalIVPut(
                        S=stock_price, K=K[k], T=tau, r=r, p=true_option_put['Close'].iloc[k])
                    iv = iv + [implied_vol]
                    delta = delta + \
                        [CalDeltaPut(S=stock_price, K=K[k],
                                     T=tau, r=r, iv=implied_vol)]
                    gamma = gamma + \
                        [CalGammaPut(S=stock_price, K=K[k],
                                     T=tau, r=r, iv=implied_vol)]
                    vega = vega + \
                        [CalVegaPut(S=stock_price, K=K[k], T=tau, r=r, iv=implied_vol)]
                    vanna = vanna + \
                        [CalVannaPutPct(S=stock_price, K=K[k],
                                        T=tau, r=r, iv=implied_vol)]
        df1['iv'] = iv
        df1['delta'] = delta
        df1['gamma'] = gamma
        df1['vega'] = vega
        df1['vanna'] = vanna
        # compute 300
        df2 = pd.DataFrame()
        l = len(date)
        delta = []
        iv = []
        gamma = []
        vega = []
        vanna = []
        for j in range(l):
            crt_date = date[j]
            print(f'computing:{crt_date}')
            true_option_all = data_300.loc[(data_300.index == crt_date)]
            maturity = true_option_all['maturity']\
                .drop_duplicates(keep='first').tolist()
            maturity.sort()
            for i in range(4):
                true_option = true_option_all\
                    .loc[list(true_option_all['maturity'] == maturity[i]), :]
                if df2.empty:
                    df2 = true_option
                else:
                    df2 = df2.append(true_option)
                crt_bool = ['.C.' in true_option['code'][i]
                            for i in range(len(true_option))]
                true_option_call = true_option[crt_bool]
                crt_bool_put = ['.P.' in true_option['code'][i]
                                for i in range(len(true_option))]
                true_option_put = true_option[crt_bool_put]
                K = [float(i) for i in np.array(true_option_call['strike'])]
                K = np.array(K)
                try:
                    tau = true_option.tau.iloc[0]/244
                except IndexError:
                    print('Error:wrong tau')
                iiidd = np.abs(true_option_call['Close']
                               - true_option_put['Close']).argmin()
                stock_price = (np.array(true_option_call['Close'])
                               + K*np.exp(-tau*r)
                               - np.array(true_option_put['Close']))[iiidd]
                for k in range(len(true_option_call)):
                    implied_vol = CalIVCall(
                        S=stock_price, K=K[k], T=tau, r=r, c=true_option_call['Close'].iloc[k])
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
                for k in range(len(true_option_put)):
                    implied_vol = CalIVPut(
                        S=stock_price, K=K[k], T=tau, r=r, p=true_option_put['Close'].iloc[k])
                    iv = iv + [implied_vol]
                    delta = delta + \
                        [CalDeltaPut(S=stock_price, K=K[k],
                                     T=tau, r=r, iv=implied_vol)]
                    gamma = gamma + \
                        [CalGammaPut(S=stock_price, K=K[k],
                                     T=tau, r=r, iv=implied_vol)]
                    vega = vega + \
                        [CalVegaPut(S=stock_price, K=K[k], T=tau, r=r, iv=implied_vol)]
                    vanna = vanna + \
                        [CalVannaPutPct(S=stock_price, K=K[k],
                                        T=tau, r=r, iv=implied_vol)]
        df2['iv'] = iv
        df2['delta'] = delta
        df2['gamma'] = gamma
        df2['vega'] = vega
        df2['vanna'] = vanna
        flag = []
        for i in range(len(df1)):
            if '.C.' in df1['code'][i]:
                flag = flag+['C']
            else:
                flag = flag+['P']
        df1['flag'] = flag
        flag = []
        for i in range(len(df2)):
            if '.C.' in df2['code'][i]:
                flag = flag+['C']
            else:
                flag = flag+['P']
        df2['flag'] = flag
        del df1['DateTime']
        del df2['DateTime']
        print('计算完毕!')
        end = time.perf_counter()
        spend = end-start_time
        print(f'更新数据共耗时{spend}')
        df_50_final = df_50_old.append(df1)
        df_50_final.index = df_50_final['date']
        # df_50_final.drop(['date.1'],axis=1,inplace=True)
        df_300_final = df_300_old.append(df2)
        df_300_final.index = df_300_final['date']
        # df_300_final.drop(['date.1'],axis=1,inplace=True)
        print('开始保存数据')
        df_50_final.to_hdf(files['A'],key='1')
        df_300_final.to_hdf(files['E'],key='1')
        etf_50_new.to_hdf(files['C'],key='1')
        etf_300_new.to_hdf(files['D'],key='1')
        print('保存成功!')

if __name__ == '__main__':
    update()