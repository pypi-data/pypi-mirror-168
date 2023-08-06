#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   read_hdf.py
@Time    :   2022/01/15 15:46:05
@Author  :   DingWenjie
@Contact :   359582058@qq.com
@Desc    :   None
'''

import pandas as pd
import os

pt = os.path.dirname(os.path.realpath(__file__))
files = {
        'A': os.path.join(pt, 'get_data_from_wind/option_50_data_wind.h5'),
        'B': os.path.join(pt, 'get_data_from_wind/etf_50_data_wind.h5'),
        'C': os.path.join(pt, 'get_data_from_qfx/option_data_50.h5'),
        'D': os.path.join(pt, 'get_data_from_qfx/option_data_300.h5'),
        'E': os.path.join(pt, 'get_data_from_qfx/etf_50.h5'),
        'F': os.path.join(pt, 'get_data_from_qfx/etf_300.h5'),
}
def read_data_wind():
    option_data = pd.read_hdf(files['A'])
    etf_data = pd.read_hdf(files['B'])
    return option_data, etf_data

def read_data_qfx_300():
    option_data = pd.read_hdf(files['D'])
    etf_data = pd.read_hdf(files['F'])
    return option_data, etf_data

def read_data_qfx_50():
    option_data = pd.read_hdf(files['C'])
    etf_data = pd.read_hdf(files['E'])
    return option_data, etf_data

if __name__ == '__main__':
    pass