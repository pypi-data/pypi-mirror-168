#usr JiangYu
import time
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
from skimage import transform,filters
import matplotlib.patches as mpatches
from skimage import transform,filters,segmentation,measure,morphology
from scipy import signal,misc,ndimage
import astropy.io.fits as fits
import astropy.wcs as wcs
import tabulate

from ConBased import ConBased_2D
from ConBased import ConBased_3D


def get_wcs(data_name):
    """
    得到wcs信息
    :param data_name: fits文件
    :return:
    data_wcs
    """
    data_header = fits.getheader(data_name)
    keys = data_header.keys()
    key = [k for k in keys if k.endswith('4')]
    [data_header.remove(k) for k in key]

    try:
        data_header.remove('VELREF')
    except:
        pass
    data_header['NAXIS'] = 3
    data_wcs = wcs.WCS(data_header)

    return data_wcs

def change_pix2word(data_wcs, outcat, ndim):
    """
    将算法检测的结果(像素单位)转换到天空坐标系上去
    :param data_wcs: 头文件得到的wcs
    :param outcat: 算法检测核表
    :return:
    outcat_wcs
    ['ID', 'Peak1', 'Peak2', 'Peak3', 'Cen1', 'Cen2', 'Cen3', 'Size1', 'Size2', 'Size3', 'Peak', 'Sum', 'Volume'] -->3d
     ['ID', 'Peak1', 'Peak2', 'Cen1', 'Cen2',  'Size1', 'Size2', 'Peak', 'Sum', 'Volume']-->2d
    """
    outcat_column = outcat.shape[1]

    if ndim == 2:
        # 2d result
        peak1, peak2 = data_wcs.all_pix2world(outcat['Peak1'], outcat['Peak2'], 1)
        clump_Peak = np.column_stack([peak1, peak2])
        cen1, cen2 = data_wcs.all_pix2world(outcat['Cen1'], outcat['Cen2'], 1)
        clump_Cen = np.column_stack([cen1, cen2])
        size1, size2 = np.array([outcat['Size1'] * 30, outcat['Size2'] * 30])
        clustSize = np.column_stack([size1, size2])
        clustPeak, clustSum, clustVolume = np.array([outcat['Peak'], outcat['Sum'], outcat['Volume']])
        id_clumps = []  # MWSIP017.558+00.150+020.17  分别表示：银经：17.558°， 银纬：0.15°，速度：20.17km/s
        for item_l, item_b in zip(cen1, cen2):
            str_l = 'MWSIP' + ('%.03f' % item_l).rjust(7, '0')
            if item_b < 0:
                str_b = '-' + ('%.03f' % abs(item_b)).rjust(6, '0')
            else:
                str_b = '+' + ('%.03f' % abs(item_b)).rjust(6, '0')
            id_clumps.append(str_l + str_b)
        id_clumps = np.array(id_clumps)

    elif ndim == 3:
        # 3d result
        peak1, peak2, peak3 = data_wcs.all_pix2world(outcat['Peak1'], outcat['Peak2'], outcat['Peak3'], 1)
        clump_Peak = np.column_stack([peak1, peak2, peak3 / 1000])
        cen1, cen2, cen3 = data_wcs.all_pix2world(outcat['Cen1'], outcat['Cen2'], outcat['Cen3'], 1)
        clump_Cen = np.column_stack([cen1, cen2, cen3 / 1000])
        size1, size2, size3 = np.array([outcat['Size1'] * 30, outcat['Size2'] * 30, outcat['Size3'] * 0.166])
        clustSize = np.column_stack([size1, size2, size3])
        clustPeak, clustSum, clustVolume = np.array([outcat['Peak'], outcat['Sum'], outcat['Volume']])

        id_clumps = []  # G017.558+00.150+020.17  分别表示：银经：17.558°， 银纬：0.15°，速度：20.17km/s
        for item_l, item_b, item_v in zip(cen1, cen2, cen3 / 1000):
            str_l = 'MWISP' + ('%.03f' % item_l).rjust(7, '0')
            if item_b < 0:
                str_b = '-' + ('%.03f' % abs(item_b)).rjust(6, '0')
            else:
                str_b = '+' + ('%.03f' % abs(item_b)).rjust(6, '0')
            if item_v < 0:
                str_v = '-' + ('%.03f' % abs(item_v)).rjust(6, '0')
            else:
                str_v = '+' + ('%.03f' % abs(item_v)).rjust(6, '0')
            id_clumps.append(str_l + str_b + str_v)
        id_clumps = np.array(id_clumps)
    else:
        print('outcat columns is %d' % outcat_column)
        return None

    outcat_wcs = np.column_stack((id_clumps, clump_Peak, clump_Cen, clustSize, clustPeak, clustSum, clustVolume))
    return outcat_wcs

def to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)

def save_outcat(outcat_name, outcat, ndim):
    """
    :param outcat_name: 核表的路径
    :param outcat: 核表数据
    :return:
    """
    outcat_colums = outcat.shape[1]
    pd.DataFrame.to_fwf = to_fwf
    if ndim == 2:
        # 2d result
        table_title = ['ID', 'Peak1', 'Peak2', 'Cen1', 'Cen2', 'Size1', 'Size2',
                       'Peak', 'Sum', 'Volume', 'Angle', 'Edge']
        dataframe = pd.DataFrame(outcat, columns=table_title)
        dataframe = dataframe.round({'ID': 0, 'Peak1': 0, 'Peak2': 0, 'Cen1': 3, 'Cen2': 3,
                                     'Size1': 3, 'Size2': 3, 'Peak': 3, 'Sum': 3, 'Volume': 0,
                                     'Angle': 2, 'Edge':0})
        dataframe.to_csv(outcat_name, sep='\t', index=False)
        # dataframe.to_fwf(detected_outcat_name)
    elif ndim == 3:
        # 3d result
        table_title = ['ID', 'Peak1', 'Peak2', 'Peak3', 'Cen1', 'Cen2', 'Cen3', 'Size1', 'Size2', 'Size3', 'Peak',
                       'Sum', 'Volume', 'Angle', 'Edge']
        dataframe = pd.DataFrame(outcat, columns=table_title)
        dataframe = dataframe.round({'ID': 0, 'Peak1': 0, 'Peak2': 0, 'Peak3': 0, 'Cen1': 3, 'Cen2': 3, 'Cen3': 3,
                                     'Size1': 3, 'Size2': 3, 'Size3': 3, 'Peak': 3, 'Sum': 3, 'Volume': 3,
                                     'Angle': 2, 'Edge':0})
        dataframe.to_csv(outcat_name, sep='\t', index=False)
        # dataframe.to_fwf(detected_outcat_name)

        print('outcat columns is %d' % outcat_colums)

def Table_Interface(did_table, ndim):
    Peak = did_table['peak_value']
    Sum = np.array(did_table['clump_sum'])
    Volume = np.array(did_table['clump_volume'])
    Angle = np.array(did_table['clump_angle'])
    Edge = np.array(did_table['clump_edge'])
    if ndim == 2:
        Peak1 = np.array(did_table['peak_location'])[:, 1] + 1
        Peak2 = np.array(did_table['peak_location'])[:, 0] + 1
        Cen1 = np.array(did_table['clump_com'])[:, 1] + 1
        Cen2 = np.array(did_table['clump_com'])[:, 0] + 1
        Size1 = np.array(did_table['clump_size'])[:, 1]
        Size2 = np.array(did_table['clump_size'])[:, 0]
        index_id = np.array(range(1, len(Peak1) + 1, 1))
        d_outcat = np.hstack(
            [[index_id, Peak1, Peak2, Cen1, Cen2, Size1, Size2, Peak, Sum, Volume, Angle, Edge]]).T
        df_outcat = pd.DataFrame(d_outcat, columns= \
            ['ID', 'Peak1', 'Peak2', 'Cen1', 'Cen2', 'Size1', 'Size2', 'Peak', 'Sum', 'Volume', 'Angle', 'Edge'])
    elif ndim == 3:
        Peak1 = np.array(did_table['peak_location'])[:, 2] + 1
        Peak2 = np.array(did_table['peak_location'])[:, 1] + 1
        Peak3 = np.array(did_table['peak_location'])[:, 0] + 1
        Cen1 = np.array(did_table['clump_com'])[:, 2] + 1
        Cen2 = np.array(did_table['clump_com'])[:, 1] + 1
        Cen3 = np.array(did_table['clump_com'])[:, 0] + 1
        Size1 = np.array(did_table['clump_size'])[:, 2]
        Size2 = np.array(did_table['clump_size'])[:, 1]
        Size3 = np.array(did_table['clump_size'])[:, 0]

        index_id = np.array(range(1, len(Peak1) + 1, 1))
        d_outcat = np.hstack([[index_id, Peak1, Peak2, Peak3, Cen1, Cen2, Cen3, Size1, Size2, Size3,
                               Peak, Sum, Volume, Angle, Edge]]).T
        df_outcat = pd.DataFrame(d_outcat, columns= \
            ['ID', 'Peak1', 'Peak2', 'Peak3', 'Cen1', 'Cen2', 'Cen3', 'Size1', 'Size2', 'Size3',
             'Peak', 'Sum', 'Volume', 'Angle', 'Edge'])
    return df_outcat

def Detect(file_name, parameters, mask_name, outcat_name, outcat_wcs_name):
    global did_table
    start_1 = time.time()
    start_2 = time.ctime()
    RMS = parameters[0]
    Threshold = parameters[1]
    RegionMin = parameters[2]
    ClumpMin = parameters[3]
    DIntensity = parameters[4]
    DDistance = parameters[5]
    origin_data = fits.getdata(file_name)
    ndim = origin_data.ndim
    if ndim==2:
        did_table = ConBased_2D.Detect_ConBased(RMS, Threshold, RegionMin[0], ClumpMin[0], DIntensity, DDistance[0], origin_data)
    elif ndim==3:
        did_table = ConBased_3D.Detect_ConBased(RMS, Threshold, RegionMin, ClumpMin, DIntensity, DDistance, origin_data)
    else:
        print('Please check the dimensionality of the data!')
    np.savez('ConBased_'+outcat_name[:-4] + '_npz', did_ConBased=did_table)
    regions_data = did_table['regions_data']
    fits.writeto(mask_name, regions_data, overwrite=True)
    df_outcat = Table_Interface(did_table, ndim)
    df_outcat.to_csv(outcat_name, sep='\t', index=False)

    data_wcs = get_wcs(file_name)
    outcat_wcs = change_pix2word(data_wcs, df_outcat, ndim)
    save_outcat(outcat_name=outcat_wcs_name, outcat=outcat_wcs, ndim=ndim)

    end_1 = time.time()
    end_2 = time.ctime()
    delta_time = end_1 - start_1

    time_record = np.hstack([[start_2, end_2, delta_time]])
    time_record = pd.DataFrame(time_record, index=['Start', 'End', 'DTime'])
    time_record.to_csv('ConBased_'+outcat_name[:-4] + '_time_record.txt', sep='\t', index=False)
    print('Time:', delta_time)
    return did_table

if __name__ == '__main__':
    #2D、3D
    RMS = 0.23
    Threshold = 2 * RMS  # ['mean','otsu',n*RMS]
    RegionMin = 27 # [9,18,27],[27,64,125]
    ClumpMin = 216 # [27,...]，[125,...]
    DIntensity = 2 * RMS # [-3*RMS,3*RMS]
    DDistance = 8 # [4,16]

    parameters = [RMS, Threshold, RegionMin, ClumpMin, DIntensity, DDistance]
    file_name = 'file_name'
    mask_name = 'mask.fits'
    outcat_name = 'outcat.txt'
    outcat_wcs_name = 'outcat_wcs.txt'
    did_ConBased = Detect(file_name, parameters, mask_name, outcat_name, outcat_wcs_name)


