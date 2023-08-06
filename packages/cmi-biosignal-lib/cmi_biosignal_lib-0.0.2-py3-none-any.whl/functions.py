import datetime
import os
import time
from datetime import datetime
import re
import glob
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler
# from multiprocessing import Pool
import multiprocessing
from scipy.fft import rfft
import numpy as np
import torch
from scipy.fft import rfft
import biosppy as bs
import pyhrv.time_domain as td
import pyhrv.frequency_domain as fd
import pyhrv.nonlinear as nl
import neurokit2
from scipy.stats import kurtosis, skew

class Biosignal_lib():
    def __init__(self, root_dir, operating_system):
        self.root_dir = root_dir
        self.operating_system = operating_system

    def Three_element_sum(self, a, n):
        b = []
        for i in range(0, n, 3):
            if (i == n - 1):
                b.append(a[i])
            else:
                b.append(a[i] + ':' + a[i + 1] + ':' + a[i + 2])

        return b



    def make_wave_list_df(self, data_path, save_path):
        '''
        :param root_dir: base directory
        :param os: 'windows' , 'linux', 'mac' (default)
        :return: wave list dataframe [columns = 'intime', 'outtime', 'starttime', 'endtime', 'wave_type']
        '''
        wave_list = []
        data_path = data_path
        save_path = save_path
        oskind = self.operating_system
        for (root, dirs, files) in os.walk(data_path):
            # print("# root : " + root)
            wave_list.extend(glob.glob(f'{root}/*.csv'))
            self.wave_list_df = pd.DataFrame({'path': wave_list})
        if oskind == 'mac':
            ## macos에서는 파일명의 콜론이 자동으로 언더바로 바뀜
            self.wave_list_df = pd.concat([self.wave_list_df,
                                      pd.DataFrame(
                                          self.wave_list_df['path'].str.replace(f'{data_path}', '').str.split('/').to_list(),
                                          columns=['pat_id', 'filename'])],
                                     axis=1)
            print(self.wave_list_df)
            tmp = self.wave_list_df['filename'].str.replace('.csv', '').str.split('_').tolist()
            print(tmp)
            rslt = []
            for i in range(len(tmp)):
                rslt.append(self.Three_element_sum(tmp[i], 13))
            self.wave_list_df = pd.concat([self.wave_list_df, pd.DataFrame(rslt, columns=['intime', 'outtime', 'starttime', 'endtime', 'wave_type'])], axis=1)
            del tmp
            del rslt

            self.wave_list_df.to_csv(f'{save_path}wave_list_df_{datetime.now()}.csv')


            return self.wave_list_df

        else:
            self.wave_list_df = pd.concat([self.wave_list_df,
                                      pd.DataFrame(
                                          self.wave_list_df['path'].str.replace(f'{root_dir}', '').str.split('/').to_list(),
                                          columns=['pat_id', 'filename'])],
                                     axis=1)
            self.wave_list_df = pd.concat([self.wave_list_df,
                                      pd.DataFrame(
                                          self.wave_list_df['filename'].str.replace('.csv', '').str.split('_').to_list(),
                                          columns=['intime', 'outtime', 'starttime', 'endtime', 'wave_type'])],
                                     axis=1)
            self.wave_list_df.to_csv(f'{root_dir}wave_list_df_{datetime.datetime.now()}.csv')

            return self.wave_list_df
    #         if len(dirs) > 0:
    #             for dir_name in dirs:
    #                 pass
    #                 #print("dir: " + dir_name)

    #         if len(files) > 0:
    #             for file_name in files:
    #                 pass
    # print("file: " + root + '/' +file_name)

    def read_wavelist_df(self, filepath):
        self.wave_list_df = pd.read_csv(filepath,
                                   dtype={"pat_id": object}, parse_dates=["intime", "outtime", "starttime", "endtime"])
        self.wave_list_df.drop(["Unnamed: 0"], axis=1, inplace=True)
        return self.wave_list_df

    def extract_shape_feature(self, wave, front=None):
        if wave.ndim == 1:
            wave = wave.reshape(-1, 1)

        front = '' if front is None else front + '_'

        transformer = RobustScaler()
        scaled_wave = transformer.fit_transform(wave)
        scaled_wave = scaled_wave.squeeze()

        activity, morbidity, complexity = self.hjorth(scaled_wave)
        kurt = kurtosis(scaled_wave, nan_policy='omit')
        skewness = skew(scaled_wave, nan_policy='omit')
        if not (type(skewness) is float):
            skewness = float(skewness.data)
        return activity, morbidity, complexity, kurt, skewness

    def hjorth(self, wave):
        first_deriv = np.diff(wave)
        second_deriv = np.diff(wave, 2)

        var_zero = np.nanmean(wave ** 2)
        var_d1 = np.nanmean(first_deriv ** 2)
        var_d2 = np.nanmean(second_deriv ** 2)

        activity = var_zero
        morbidity = np.sqrt(var_d1 / var_zero)
        complexity = np.sqrt(var_d2 / var_d1) / morbidity

        return activity, morbidity, complexity

    def get_last_8seconds(self, row):
        if not os.path.exists(row['path']):
            return None

        # 한 파일 불러오기
        wave_data = pd.read_csv(row['path'], index_col=0, parse_dates=['start_time'])
        # print(wave_data['start_time'].min(), wave_data['start_time'].max())
        if len(wave_data) == 0:
            return None

        if row['wave_type'] == 'II':
            # 대략 뒤 20초 먼저 자르기
            wave_data = wave_data.loc[(wave_data['start_time'] < row['endtime']) & (
                        wave_data['start_time'] >= (row['endtime'] - pd.Timedelta(seconds=20)))]

            if len(wave_data) == 0:
                return None

            duration = (wave_data['start_time'] - wave_data['start_time'].shift(1)).median()
            # print(duration)

            # index가 timestamp, 한 컬럼이 waveform값인 dataframe 만들기
            # wv = pd.DataFrame({'signal': np.array([eval(ls) for ls in wave_data['data_array'].tolist()]).reshape(-1)})
            wv = pd.DataFrame({'signal': np.concatenate([eval(ls) for ls in wave_data['data_array']]).reshape(-1)})
            wvstart = wave_data['start_time'].min()
            wvend = wave_data['start_time'].max() + duration
            n_data = len(wv)
            obs_hz = n_data / (wvend - wvstart).total_seconds()
            # print('observed_hz =', obs_hz, 'total data point', n_data)

            wv.index = [pd.Timestamp.fromtimestamp(i, tz='utc') for i in np.arange(wvstart.timestamp(),
                                                                                   wvend.timestamp(), step=1 / obs_hz)][
                       :n_data]
            # print(row['wave_type'])

            # resampling to 250 Hz
            wv = wv.resample('0.004S').median()  # 1/250
            if len(wv) < 2048:
                return None
            last8s = wv['signal'].to_numpy()[-2048:]
            return last8s

        elif row['wave_type'] == 'Pleth':
            wave_data = wave_data.loc[(wave_data['start_time'] < row['endtime']) & (
                        wave_data['start_time'] >= (row['endtime'] - pd.Timedelta(seconds=20)))]

            if len(wave_data) == 0:
                return None

            duration = (wave_data['start_time'] - wave_data['start_time'].shift(1)).median()
            # print(duration)

            # index가 timestamp, 한 컬럼이 waveform값인 dataframe 만들기
            # wv = pd.DataFrame({'signal': np.array([eval(ls) for ls in wave_data['data_array'].tolist()]).reshape(-1)})
            wv = pd.DataFrame({'signal': np.concatenate([eval(ls) for ls in wave_data['data_array']]).reshape(-1)})
            wvstart = wave_data['start_time'].min()
            wvend = wave_data['start_time'].max() + duration
            n_data = len(wv)
            obs_hz = n_data / (wvend - wvstart).total_seconds()
            # print('observed_hz =', obs_hz, 'total data point', n_data)

            wv.index = [pd.Timestamp.fromtimestamp(i, tz='utc') for i in np.arange(wvstart.timestamp(),
                                                                                   wvend.timestamp(), step=1 / obs_hz)][
                       :n_data]
            # print(row['wave_type'])

            # resampling to 250 Hz
            wv = wv.resample('0.008S').median()  # 1/125
            if len(wv) < 2048:
                return None
            last8s = wv['signal'].to_numpy()[-2048:]
            return last8s

    def shape_feature_process_one_waveform(self, idx):
        # print(idx)
        wave = None
        data = None

        row = self.wave_list_df.iloc[idx]
        try:
            wave = self.get_last_8seconds(row)
        except Exception as e:
            print('error in ', idx, 'get_last_8seconds')
            print(e)
        try:
            if wave is not None:
                data = self.extract_shape_feature(wave)
                return tuple([row['path']])+data
        except Exception as e:
            print('error in ', idx, 'extract_shape_feature')
            print(e)
        return tuple([row['path'], data])

    def get_shape_feature_rslt(self, tmp_dir, mp = 'on', n_unit=10000, processes = 40):
        '''
        extract_shape_feature and write each 1000 files
        :param tmp_dir:
        :param mp:
        :return:
        '''
        wave_list_df = self.wave_list_df
        nowDate = datetime.now().strftime("%Y%m%d")
        since = time.time()
        n_unit = n_unit
        if mp == 'on':
            for i in range(int(len(wave_list_df)/n_unit)):
                partial_range = range(i*n_unit, min(n_unit*i+n_unit, len(wave_list_df)))
                print(min(partial_range), max(partial_range))
                pool = multiprocessing.Pool(processes=processes)
                outputs = pool.map(self.shape_feature_process_one_waveform, partial_range)
                result_path = tmp_dir+f'/shape_feature_{nowDate}_{min(partial_range)}-{max(partial_range)}.csv'
                pd.DataFrame(outputs).to_csv(result_path, index=False)
                print(min(partial_range), max(partial_range), 'elapsed', (time.time()-since)/60, 'minutes')
#
        else:
            pass

        shape_feature_names = ['hjorth_activity', 'hjorth_morbidity', 'hjorth_complexity', 'kurtosis', 'skewness']
        shapefiles = os.listdir(tmp_dir)
        df_list = []
        for f in shapefiles:
            if f == '.DS_Store':
                continue
            else:
                df = pd.read_csv(os.path.join(tmp_dir, f))
                df_list.append(df)
        df = pd.concat(df_list)
        df.columns = ['path']+shape_feature_names

        return df

    def hrv_process_one_waveform(self, idx):
        # print(idx)
        wave = None
        data = None

        row = self.wave_list_df.iloc[idx]
        wave_type = row['wave_type']

        if wave_type == 'II':
            try:
                wave = self.get_last_8seconds(row)
            except Exception as e:
                print('error in ', idx, 'get_last_8seconds')
                print(e)
            try:
                ECG = wave
                t = torch.FloatTensor(ECG)
                t = t.view(-1, 1, 2048)  # 10 min * 18 step
                t = t[:, :, -2048:]

                bs_process = bs.signals.ecg.ecg(signal=ECG, sampling_rate=250, show=False)
                sig = bs_process[0]
                filtered_signal = bs_process[1]
                rpeaks = bs_process[2]

                if wave is not None:
                    ## td : sdnn, rmssd, sdsd, sdann, pnn50, pnn20
                    ## fd : VLF_peak, LF_peak, HF_peak, VLF, LF, HF, LF_HF, VLF_rel, LF_rel, HF_rel
                    ## nl : sd1, sd2, sd_ratio, SampEn, a1, a2, a_ratio
                    td_data = self.hrv_td(sig, rpeaks)######################sampling rate
                    print(idx, tuple([row['path']]) + td_data)
                    fd_data = self.hrv_fd(sig, rpeaks)
                    nl_data = self.hrv_nl(sig, rpeaks)

                    return tuple([row['path']]) + td_data# + fd_data + nl_data
            except Exception as e:
                print('error in ', idx, 'hrv_td , hrv_fd, hrv_nl')
                print(e)
            return tuple([row['path'], data])

        elif wave_type == 'Pleth':
            try:
                wave = self.get_last_8seconds(row)
            except Exception as e:
                print('error in ', idx, 'get_last_8seconds')
                print(e)
            try:
                PPG = wave
                t = torch.FloatTensor(PPG)
                t = t.view(-1, 1, 2048)  # 10 min * 18 step
                t = t[:, :, -1024:]
                signals, info = neurokit2.ppg.ppg_process(PPG, sampling_rate=125)

                if wave is not None:
                    ## td : sdnn, rmssd, sdsd, sdann, pnn50, pnn20
                    ## fd : VLF_peak, LF_peak, HF_peak, VLF, LF, HF, LF_HF, VLF_rel, LF_rel, HF_rel
                    ## nl : sd1, sd2, sd_ratio, SampEn, a1, a2, a_ratio
                    td_data = self.hrv_td(PPG, info['PPG_Peaks'])######################sampling rate
                    fd_data = self.hrv_fd(PPG, info['PPG_Peaks'])
                    nl_data = self.hrv_nl(PPG, info['PPG_Peaks'])
                    return tuple([row['path']]) + td_data + fd_data + nl_data
            except Exception as e:
                print('error in ', idx, 'hrv_td , hrv_fd, hrv_nl')
                print(e)
            return tuple([row['path'], data])
        else:
            return tuple([row['path'], data])

    def get_hrv_feature_rslt(self, tmp_dir, mp = 'on', n_unit=10000, processes = 40):
        '''
        extract_shape_feature and write each 1000 files
        :param tmp_dir:
        :param mp:
        :return:
        '''
        wave_list_df = self.wave_list_df
        nowDate = datetime.now().strftime("%Y%m%d")
        since = time.time()
        n_unit = n_unit
        if mp == 'on':
            for i in range(int(len(wave_list_df) / n_unit)):
                partial_range = range(i * n_unit, min(n_unit * i + n_unit, len(wave_list_df)))
                print(min(partial_range), max(partial_range))

                pool = multiprocessing.Pool(processes=processes)
                outputs = pool.map(self.hrv_process_one_waveform, partial_range)

                result_path = tmp_dir + f'/hrv_feature_{nowDate}_{min(partial_range)}-{max(partial_range)}.csv'
                rslt_df = pd.DataFrame(outputs)
                rslt_df.to_csv(result_path, index=False)
                print(min(partial_range), max(partial_range), 'elapsed', (time.time() - since) / 60, 'minutes')
        #
        else:
            pass
        ## td : sdnn, rmssd, sdsd, sdann, pnn50, pnn20
        ## fd : VLF_peak, LF_peak, HF_peak, VLF, LF, HF, LF_HF, VLF_rel, LF_rel, HF_rel
        ## nl : sd1, sd2, sd_ratio, SampEn, a1, a2, a_ratio

        # hrv_feature_names = ['sdnn', 'rmssd', 'sdsd', 'sdann', 'pnn50', 'pnn20']

        hrv_feature_names = ['sdnn', 'rmssd', 'sdsd', 'sdann', 'pnn50', 'pnn20', 'VLF_peak', 'LF_peak',
                             'HF_peak', 'VLF', 'LF', 'HF', 'LF_HF', 'VLF_rel', 'LF_rel', 'HF_rel', 'sd1', 'sd2',
                             'sd_ratio', 'SampEn', 'a1', 'a2', 'a_ratio']
        hrvfiles = os.listdir(tmp_dir)
        df_list = []
        for f in hrvfiles:
            if f == '.DS_Store':
                continue
            else:
                df = pd.read_csv(os.path.join(tmp_dir, f))
                df_list.append(df)
        df = pd.concat(df_list)
        df.columns = ['path'] + hrv_feature_names

        return df

    def hrv_td(self, sig, rpeaks):
        sdnn = round(td.sdnn(rpeaks=rpeaks)[0], 3)  # 0
        rmssd = round(td.rmssd(rpeaks=rpeaks)[0], 3)  # 1
        sdsd = round(td.sdsd(rpeaks=rpeaks)[0], 3)  # 2
        sdann = round(td.sdann(rpeaks=rpeaks)[0], 3)  # 3
        pnn50 = round(td.nn50(rpeaks=rpeaks)[1], 3)  # 4
        pnn20 = round(td.nn20(rpeaks=rpeaks)[1], 3)  # 5

        return sdnn, rmssd, sdsd, sdann, pnn50, pnn20

    def hrv_fd(self, sig, rpeaks):  ########################################sampling rate
        abs_results = fd.lomb_psd(rpeaks=sig[rpeaks], show=False)
        plt.close()
        # peak
        VLF_peak = round(abs_results[1][0], 3)  # 0
        LF_peak = round(abs_results[1][1], 3)  # 1
        HF_peak = round(abs_results[1][2], 3)  # 2

        # Abs Power
        VLF = round(abs_results[2][0], 3)  # 3
        LF = round(abs_results[2][1], 3)  # 4
        HF = round(abs_results[2][2], 3)  # 5
        LF_HF = round((LF / HF), 3)  # 6

        # Relatives
        VLF_rel = round(abs_results[3][0], 3)  # 7
        LF_rel = round(abs_results[3][1], 3)  # 8
        HF_rel = round(abs_results[3][2], 3)  # 9

        return VLF_peak, LF_peak, HF_peak, VLF, LF, HF, LF_HF, VLF_rel, LF_rel, HF_rel

    def hrv_nl(self, sig, rpeaks):  ##########################################3
        # poincare
        poincare_results = nl.poincare(rpeaks=sig[rpeaks], show=False)
        plt.close()
        sd1 = round(poincare_results['sd1'], 3)  # 0
        sd2 = round(poincare_results['sd2'], 3)  # 1
        sd_ratio = round(poincare_results['sd_ratio'], 3)  # 2

        # SampEn
        SampEn = round(nl.sample_entropy(rpeaks=rpeaks)[0], 3)  # 3

        # DFA
        DFA = nl.dfa(rpeaks=sig[rpeaks], show=False)  # 4
        plt.close()
        if DFA['dfa_alpha1'] == 'nan' and DFA['dfa_alpha2']:
            a1 = DFA['dfa_alpha1']
            a2 = DFA['dfa_alpha2']
            a_ratio = 'nan'

        else:
            a1 = round(DFA['dfa_alpha1'][0], 3)  # 5
            a2 = round(DFA['dfa_alpha2'][0], 3)  # 6
            a_ratio = round(a1 / a2, 3)  # 7

        return sd1, sd2, sd_ratio, SampEn, a1, a2, a_ratio
