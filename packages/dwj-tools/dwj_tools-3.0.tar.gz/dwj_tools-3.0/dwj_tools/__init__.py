'''
读取数据:
import dwj_tools.read_hdf as r
option,etf = r.read_data_wind()  # wind数据
option,etf = r.read_data_qfx_300()  # 权分析300
option,etf = r.read_data_qfx_50()  # 权分析50

更新数据:
from dwj_tools.get_data_from_wind import update_option_data_wind as u  # wind更新
from dwj_tools.get_data_from_qfx import update_data_qfx as u  # wind更新
u.update()
'''