# -*- coding: utf-8 -*-
# /usr/bin/env python

'''
Author: wenqiangw
Email: wqwangchn@163.com
Date: 2022/9/21 19:01
Desc:
'''

import datetime
import os

import numpy as np
import pandas as pd
# 策略交叉评估

class RiskStrategy:
    def __init__(self, sample_ratio_list=[0.49], fee_ratio_list=[0.8], report_ratio_list=[0.5],
                 bad_ratio_interval=[0.15, 0.25]):
        '''

        :param sample_ratio_list:
        :param fee_ratio_list:
        :param report_ratio_list:
        :param bad_ratio_interval:
        '''
        self.INIT_BLACK_STRATEGY = {
            'chd': [4.0],
            'zj': [1, 2]
        }
        self.sample_ratio_list = sample_ratio_list
        self.fee_ratio_list = fee_ratio_list
        self.report_ratio_list = report_ratio_list
        self.bad_ratio_interval = bad_ratio_interval
        self.strategy_report = StrategyReport()

    def check_bef_tag(self, level_x):
        '''

        :param x: 原始评分等级
        :return:
        '''
        dict_chd = {'A': 10, 'B+': 9, 'A-': 9, 'B': 8, 'B-': 7, 'B--': 7, 'C': 6, 'D': 5, 'E': 4}
        level = dict_chd.get(level_x, level_x)
        if level in range(1, 11):
            return level

    def check_aft_strategy(self, df_strategy_list, df_strategy_score):
        df_tmp = [pd.DataFrame()]
        for df_i in df_strategy_list:
            df_tmp.append(df_i.sum(axis=0).append(df_i.sum(axis=1)))
        df_concat = pd.concat(df_tmp, axis=1)
        select_index = df_concat.T.drop_duplicates().index
        df_strategy_list_sel = []
        for i in select_index:
            df_strategy_list_sel.append(df_strategy_list[i])
        df_strategy_score_sel = df_strategy_score.loc[select_index, :].reset_index(drop=True)
        return df_strategy_list_sel, df_strategy_score_sel

    def calc_level_risk(self,df_test_, by_field):
        '''

        :param df_test_: 原始数据，含保单赔付信息
        :param by_field: 分档字段
        :return:
        '''
        df_rep_tmp = df_test_.groupby(by_field).agg(
            {
                'truckno': [('样本数', lambda x: len(x)), ('车辆数', lambda x: len(set(x)))],
                'car_got': [("已赚车年", 'sum')],
                'report_num': [("出险次数", 'sum')],
                'report_fee': [("赔付金额", 'sum')],
                'fee_got': [("已赚保费", 'sum')],
            }).droplevel(0, 1).sort_index(ascending=[True, True])
        df_rep_tmp['车辆占比'] = df_rep_tmp['车辆数'] / df_rep_tmp['车辆数'].sum()
        df_rep_tmp['样本占比'] = df_rep_tmp['样本数'] / df_rep_tmp['样本数'].sum()
        df_rep_tmp['出险率'] = (df_rep_tmp['出险次数'] / df_rep_tmp['已赚车年']).apply(lambda x: round(x, 4))
        df_rep_tmp['赔付率'] = (df_rep_tmp['赔付金额'] / df_rep_tmp['已赚保费']).apply(lambda x: round(x, 4))
        df_rep_tmp['累计出险率'] = df_rep_tmp['出险次数'] * 0
        df_rep_tmp['累计赔付率'] = df_rep_tmp['出险次数'] * 0
        df_rep_tmp['累计出险率_横向'] = df_rep_tmp['出险次数'] * 0
        df_rep_tmp['累计赔付率_横向'] = df_rep_tmp['出险次数'] * 0
        df_rep_tmp['累计出险率_纵向'] = df_rep_tmp['出险次数'] * 0
        df_rep_tmp['累计赔付率_纵向'] = df_rep_tmp['出险次数'] * 0
        df_rep_tmp['累计样本占比_纵向'] = df_rep_tmp['出险次数'] * 0

        df_rep_out = df_rep_tmp.unstack() if isinstance(df_rep_tmp.index, pd.MultiIndex) else df_rep_tmp
        index = df_rep_out.index.sort_values(ascending=False)
        columns = df_rep_out.columns.sort_values(ascending=False)
        df_rep_out = df_rep_out.loc[index, columns]

        df_rep_out1 = df_rep_out[['样本占比', '出险次数', '已赚车年', '赔付金额', '已赚保费']]
        df_rep_out2 = df_rep_out1.copy()
        df_rep_out3 = df_rep_out1.copy()
        for icol in set(df_rep_out1.columns.get_level_values(0)):
            if isinstance(df_rep_tmp.index, pd.MultiIndex):
                df_rep_out1[icol] = df_rep_out1[icol].fillna(0).cumsum(axis=1)  ##横向累加
                df_rep_out2[icol] = df_rep_out2[icol].fillna(0).cumsum(axis=0)  ##纵向累加
                df_rep_out3[icol] = df_rep_out3[icol].fillna(0).cumsum(axis=1).cumsum(axis=0)  ##横向纵向累加
            else:
                df_rep_out1[icol] = df_rep_out1[icol].fillna(0)  ##横向累加
                df_rep_out2[icol] = df_rep_out2[icol].fillna(0).cumsum(axis=0)  ##纵向累加
                df_rep_out3[icol] = df_rep_out3[icol].fillna(0).cumsum(axis=0)  ##横向纵向累加

        df_rep_out['累计出险率'] = (df_rep_out3['出险次数'] / df_rep_out3['已赚车年']).apply(lambda x: round(x, 4))
        df_rep_out['累计赔付率'] = (df_rep_out3['赔付金额'] / df_rep_out3['已赚保费']).apply(lambda x: round(x, 4))
        df_rep_out['累计出险率_横向'] = (df_rep_out1['出险次数'] / df_rep_out1['已赚车年']).apply(lambda x: round(x, 4))
        df_rep_out['累计赔付率_横向'] = (df_rep_out1['赔付金额'] / df_rep_out1['已赚保费']).apply(lambda x: round(x, 4))
        df_rep_out['累计出险率_纵向'] = (df_rep_out2['出险次数'] / df_rep_out2['已赚车年']).apply(lambda x: round(x, 4))
        df_rep_out['累计赔付率_纵向'] = (df_rep_out2['赔付金额'] / df_rep_out2['已赚保费']).apply(lambda x: round(x, 4))
        df_rep_out['累计样本占比_纵向'] = df_rep_out2['样本占比']

        col_ = ['样本数', '车辆数', '样本占比', '车辆占比', '已赚车年', '已赚保费', '出险次数', '赔付金额', '出险率', '赔付率',
                '累计出险率', '累计赔付率', '累计出险率_横向', '累计出险率_纵向', '累计赔付率_横向', '累计赔付率_纵向', '累计样本占比_纵向'
                ]
        df_rep_out = df_rep_out[col_]
        return df_rep_out

    def clac_cross_strategy_white(self, df_report_test, sample_ratio_list=[0.6], fee_ratio_list=[0.6],
                                  report_ratio_list=[0.4], strategy_ordered=True):
        '''
        双模型交叉策略评估
        :param df_report_test: 评分分档赔付数据
        :param sample_ratio_list: 样本通过率 eg:[60%，65%]
        :param fee_ratio_list: 赔付率 eg:[60%，65%]
        :param report_ratio_list: 出险率 eg:[60%，65%]
        :return:
        待优化：1. 所有行的赔付率出险率阀值一样
        '''
        assert len(sample_ratio_list) > 0
        assert len(fee_ratio_list) + len(report_ratio_list) > 0
        if len(fee_ratio_list) < 1:
            fee_ratio_list = [1e6]
        if len(report_ratio_list) < 1:
            report_ratio_list = [1e6]

        df_strategy_list = []
        df_strategy_score = []
        for sample_ratio in sample_ratio_list:
            for fee_ratio in fee_ratio_list:
                for report_ratio in report_ratio_list:
                    for report_ratio_t in [report_ratio * 0.9, report_ratio, report_ratio * 1.1]:
                        for fee_ratio_t in [fee_ratio * 0.9, fee_ratio, fee_ratio * 1.1]:
                            idx2 = df_report_test.累计出险率_横向 <= report_ratio_t
                            idx3 = df_report_test.累计赔付率_横向 <= fee_ratio_t
                            idata = df_report_test[idx2 & idx3]
                            df_no_pass = idata.样本数.isna().astype(int)
                            df_no_pass_boundary = df_no_pass * (
                                (df_no_pass.shift(periods=1, axis=1) != df_no_pass).astype(int))
                            df_no_pass_boundary_cumsum = df_no_pass_boundary.cumsum(axis=1)
                            threshold_list = []
                            threshold_list.append(df_no_pass_boundary_cumsum.apply(lambda x: max(x) + 1, axis=1))
                            for i, j in df_no_pass_boundary_cumsum.iterrows():
                                for k in set(j) - set([0]):
                                    threshold_list_tmp = threshold_list.copy()
                                    for df_i in threshold_list_tmp:
                                        df_itmp = df_i.copy()
                                        df_itmp[i] = k
                                        threshold_list.append(df_itmp)
                            aa = pd.concat(threshold_list, axis=1).T.drop_duplicates()
                            for i, threshold_ in aa.iterrows():
                                df_strategy_tmp = (~(df_no_pass_boundary_cumsum.T >= threshold_).T).astype(int)
                                if strategy_ordered:
                                    df_strategy_tmp = ((df_strategy_tmp == 0).cumsum() == 0).astype(int)
                                # 策略前置条件
                                strategy_index = df_strategy_tmp.index.name
                                for i in self.INIT_BLACK_STRATEGY.get(strategy_index, []):
                                    df_strategy_tmp.loc[i, :] = 0
                                strategy_col = df_strategy_tmp.columns.name
                                for i in self.INIT_BLACK_STRATEGY.get(strategy_col, []):
                                    df_strategy_tmp.loc[:, i] = 0

                                strategy_ratio = (
                                                         df_strategy_tmp * df_report_test.样本数).sum().sum() / df_report_test.样本数.sum().sum()
                                strategy_fee = (df_strategy_tmp * df_report_test.赔付金额).sum().sum() / (
                                        df_strategy_tmp * df_report_test.已赚保费).sum().sum()
                                strategy_report = (df_strategy_tmp * df_report_test.出险次数).sum().sum() / (
                                        df_strategy_tmp * df_report_test.已赚车年).sum().sum()
                                if (strategy_ratio >= sample_ratio) & (strategy_fee <= fee_ratio) & (
                                        strategy_report <= report_ratio):
                                    df_strategy_list.append(df_strategy_tmp)
                                    df_strategy_score.append([strategy_ratio, strategy_fee, strategy_report])
        return df_strategy_list, df_strategy_score

    def clac_cross_strategy_black(self, df_report_test, sample_ratio_interval=[0.2, 0.25]):
        '''
        双模型交叉策略评估
        :param df_report_test: 评分分档赔付数据
        :param sample_ratio_interval: 样本占比区间 eg:[0.2,0.25]
        :return:
        '''
        if len(set(sample_ratio_interval)) == 1:
            sample_ratio_interval = [sample_ratio_interval - 0.03, sample_ratio_interval + 0.03]

        df_strategy_list = []
        df_strategy_score = []
        sample_ratio_start, sample_ratio_end = sample_ratio_interval

        df_strategy_ratio = df_report_test.样本数.cumsum(axis=0).cumsum(axis=1) / df_report_test.样本数.sum().sum()
        for ratio_t in range(int(max(min(sample_ratio_interval) * 100 - 10, 0)),
                             int(max(sample_ratio_interval) * 100 + 10), 2):
            ratio_t = ratio_t * 0.01
            fee_ratio = ((df_strategy_ratio > ratio_t) * df_report_test.累计赔付率).max().max()
            report_ratio = ((df_strategy_ratio > ratio_t) * df_report_test.累计出险率).max().max()
            for report_ratio_t in [report_ratio, report_ratio + 0.1, report_ratio + 0.2]:
                for fee_ratio_t in [fee_ratio + 0.2, fee_ratio + 0.1, fee_ratio, fee_ratio - 0.1]:
                    idx2 = df_report_test.累计出险率 >= report_ratio_t
                    idx3 = df_report_test.累计赔付率 >= fee_ratio_t
                    idata = df_report_test[idx2 | idx3]
                    df_no_pass = idata.样本数.isna().astype(int)
                    df_high_risk = (df_no_pass.cumsum(axis=0).cumsum(axis=1) == 0).astype(int)

                    strategy_ratio = (df_high_risk * df_report_test.样本数).sum().sum() / df_report_test.样本数.sum().sum()
                    strategy_fee = (df_high_risk * df_report_test.赔付金额).sum().sum() / (
                            df_high_risk * df_report_test.已赚保费).sum().sum()
                    strategy_report = (df_high_risk * df_report_test.出险次数).sum().sum() / (
                            df_high_risk * df_report_test.已赚车年).sum().sum()
                    if (sample_ratio_start <= strategy_ratio <= sample_ratio_end) & (strategy_fee >= fee_ratio):
                        df_strategy_list.append(df_high_risk.loc[::-1, ::-1])
                        df_strategy_score.append([strategy_ratio, strategy_fee, strategy_report])

        df_strategy_score = pd.DataFrame(df_strategy_score, columns=['通过率', '赔付率', '出险率'])
        df_strategy_list, df_strategy_score = self.check_aft_strategy(df_strategy_list, df_strategy_score)

        return df_strategy_list, df_strategy_score

    def get_single_strategy(self, df_data_, by_field, sample_ratio_list=[0.6], fee_ratio_list=[0.6], report_ratio_list=[0.4],
                            bad_ratio_interval=[0.2, 0.25]):
        '''

        :param df_report_test: 评分分档赔付数据
        :param sample_ratio_list: 样本通过率 eg:[60%，65%]
        :param fee_ratio_list: 赔付率 eg:[60%，65%]
        :param report_ratio_list: 出险率 eg:[60%，65%]
        :return:
        '''
        assert len(sample_ratio_list) > 0
        assert len(fee_ratio_list) + len(report_ratio_list) > 0
        if len(fee_ratio_list) < 1:
            fee_ratio_list = [1e6]
        if len(report_ratio_list) < 1:
            report_ratio_list = [1e6]
        df_in_ = df_data_[df_data_[by_field].isna().sum(axis=1) == 0]
        for i in by_field:
            df_in_[i] = df_in_[i].apply(self.check_bef_tag)

        if df_in_.shape[0] < 5000:
            return [], pd.DataFrame()
        df_report_test = self.calc_level_risk(df_test_=df_in_, by_field=by_field).fillna(0)

        # 白名单策略
        strategy_data = []
        for sample_ratio in [min(sample_ratio_list) - 0.05] + sample_ratio_list:
            idx1 = df_report_test.样本占比.cumsum() >= sample_ratio
            for fee_ratio in fee_ratio_list:
                for report_ratio in report_ratio_list:
                    idx2 = df_report_test.累计出险率 <= report_ratio
                    idx3 = df_report_test.累计赔付率 <= fee_ratio
                    idata = df_report_test[idx1 & idx2 & idx3]
                    strategy_data.append(idata)
        df_strategy_tmp = pd.concat(strategy_data, axis=0).drop_duplicates()
        df_strategy_score = df_strategy_tmp[['累计样本占比_纵向', '累计赔付率', '累计出险率']].sort_values('累计赔付率', ascending=True)
        df_strategy_score.columns = ['通过率', '赔付率', '出险率']

        # 黑白灰策略
        df_bwl_strategy_list = []
        for i in df_strategy_score.index:
            df_bwl_strategy = pd.DataFrame(index=df_report_test.index)
            df_bwl_strategy['bwl_tag'] = 0
            df_bwl_strategy.loc[:i, :] = 1
            for bad_growth in [0.05, 0.1, 0.15, 0.2, 0.25, 1]:
                bad_ratio_tmp = df_report_test.样本占比[::-1].cumsum().loc[::-1]
                bad_index = bad_ratio_tmp[(bad_ratio_tmp >= (min(bad_ratio_interval) - bad_growth)) & (
                (bad_ratio_tmp <= max(bad_ratio_interval) + bad_growth))].index.max()
                if (0 < bad_index < i):
                    break
            df_bwl_strategy.loc[bad_index:, :] = -1
            df_bwl_strategy_list.append(df_bwl_strategy)

        df_strategy_score = df_strategy_score.reset_index(drop=True).sort_values("赔付率")
        df_bwl_strategy_list = [df_bwl_strategy_list[i] for i in df_strategy_score.index]

        return df_bwl_strategy_list, df_strategy_score.reset_index(drop=True)

    def get_cross_strategy(self, df_data_, by_field, sample_ratio_list, fee_ratio_list, report_ratio_list,
                           bad_ratio_interval=[0.2, 0.3]):
        df_in_ = df_data_[df_data_[by_field].isna().sum(axis=1) == 0]
        if df_in_.shape[0] < 5000:
            return [], pd.DataFrame()
        for i in by_field:
            df_in_[i] = df_in_[i].apply(self.check_bef_tag)

        # 白名单策略
        df_rep_out1 = self.calc_level_risk(df_test_=df_in_, by_field=by_field).fillna(0)
        df_rep_out2 = self.calc_level_risk(df_test_=df_in_, by_field=by_field[::-1]).fillna(0)
        df_strategy_list1, df_strategy_score1 = self.clac_cross_strategy_white(df_rep_out1, sample_ratio_list,
                                                                              fee_ratio_list, report_ratio_list)
        df_strategy_list2, df_strategy_score2 = self.clac_cross_strategy_white(df_rep_out2, sample_ratio_list,
                                                                              fee_ratio_list, report_ratio_list)
        df_strategy_list = df_strategy_list1 + [i.T for i in df_strategy_list2]
        df_strategy_score = pd.DataFrame(df_strategy_score1 + df_strategy_score2, columns=['通过率', '赔付率', '出险率'])
        df_strategy_list, df_strategy_score = self.check_aft_strategy(df_strategy_list, df_strategy_score)

        # 黑名单策略
        df_in2_ = df_in_.copy()
        df_in2_[by_field] = df_in2_[by_field] * -1
        df_report_test2 = self.calc_level_risk(df_test_=df_in2_, by_field=by_field).fillna(0)
        df_report_test2.columns.set_levels(level=1, levels=df_report_test2.车辆数.columns[::-1] * -1, inplace=True)
        df_report_test2.index = df_report_test2.index * -1
        df_strategy_list_bad, df_strategy_score_bad = self.clac_cross_strategy_black(df_report_test2, bad_ratio_interval)

        # 黑白灰策略
        df_strategy_score = df_strategy_score.sort_values('赔付率', ascending=True)
        df_strategy_score_bad = df_strategy_score_bad.sort_values('赔付率', ascending=False)
        if df_strategy_score_bad.shape[0] == 0:
            print("未生成有效黑名单策略")
            return df_strategy_list, df_strategy_score
        df_bwt_strategy_list = []
        for i in df_strategy_score.index:
            df_strategy_tmp1 = (df_strategy_list[i] == 0).astype(int)
            best_j = df_strategy_score_bad.index[0]
            for j in df_strategy_score_bad.index:
                df_strategy_bad_tmp = df_strategy_tmp1 * df_strategy_list_bad[j]
                sample_ratio_tmp = ((df_rep_out1.样本数 * df_strategy_bad_tmp).sum().sum()) / (df_rep_out1.样本数.sum().sum())
                if min(bad_ratio_interval) <= sample_ratio_tmp <= max(bad_ratio_interval):
                    best_j = j
                    break
            df_bwt_strategy = df_strategy_list[i] - (df_strategy_tmp1 * df_strategy_list_bad[best_j]).fillna(1)
            df_bwt_strategy_list.append(df_bwt_strategy)

        df_strategy_score = df_strategy_score.reset_index(drop=True).sort_values("赔付率")
        df_bwl_strategy_list = [df_bwt_strategy_list[i] for i in df_strategy_score.index]

        return df_bwl_strategy_list, df_strategy_score.reset_index(drop=True)

    def get_triple_strategy(self, df_data_, by_field, sample_ratio_list, fee_ratio_list, report_ratio_list,
                            bad_ratio_interval=[0.2, 0.3]):
        assert len(by_field) == 3
        df_in_ = df_data_[df_data_[by_field].isna().sum(axis=1) == 0]
        if df_in_.shape[0] < 5000:
            return [[], []], pd.DataFrame()
        for i in by_field:
            df_in_[i] = df_in_[i].apply(self.check_bef_tag)
        bad_ratio_interval_sub = [min(bad_ratio_interval) * 0.5, max(bad_ratio_interval) * 0.7]

        df_bwt_strategy_bad, _ = self.get_single_strategy(df_in_, by_field[:1], sample_ratio_list=[0], fee_ratio_list=[1.0],
                                                     report_ratio_list=[1.0], bad_ratio_interval=bad_ratio_interval_sub)
        df_bwt_strategy_init = (df_bwt_strategy_bad[0] < 0).astype(int) * -1

        index = df_bwt_strategy_init[df_bwt_strategy_init.bwl_tag == -1].index
        df_in2_ = df_in_[~df_in_[by_field[0]].isin(index)]
        df_bwt_strategy_list_p, df_strategy_score = self.get_cross_strategy(df_in2_, by_field[1:], sample_ratio_list,
                                                                     fee_ratio_list, report_ratio_list,
                                                                     bad_ratio_interval=bad_ratio_interval_sub)

        df_strategy_score = df_strategy_score.reset_index(drop=True).sort_values("赔付率")
        df_bwt_strategy_list = [[df_bwt_strategy_init, i] for i in df_bwt_strategy_list_p]
        df_bwl_strategy_list = [df_bwt_strategy_list[i] for i in df_strategy_score.index]

        return df_bwl_strategy_list, df_strategy_score.reset_index(drop=True)

    def get_strategy_report(self, df_test_, by_field=['zj', 'chd', 'card'], dump_path=None, report_topn=50,
                            report_key='测试'):
        '''

        :param df_test_:
        :param by_field:
        :param dump_path:
        :param report_topn:
        :param report_key:
        :return:
        '''
        for i in by_field:
            df_test_[i] = df_test_[i].apply(self.check_bef_tag)

        strategy_list=[]
        score_list=[]

        df_bwt_strategy_list_s1 = []
        df_score_s1 = []
        for ifield in by_field:
            by_field1 = [ifield]
            df_bwt_strategy_list1, df_strategy_score1 = self.get_single_strategy(df_test_, by_field1, self.sample_ratio_list,
                                                                            self.fee_ratio_list, self.report_ratio_list,
                                                                            self.bad_ratio_interval)
            df_bwt_strategy_list_s1.extend(df_bwt_strategy_list1)
            df_score_s1.append(df_strategy_score1)

        df_score_s1 = pd.concat(df_score_s1).reset_index(drop=True).sort_values("赔付率")
        df_bwt_strategy_list_s1 = [df_bwt_strategy_list_s1[i] for i in df_score_s1.index]
        strategy_list.append(df_bwt_strategy_list_s1)
        score_list.append(df_score_s1.reset_index(drop=True))

        if len(by_field)>1:
            df_bwt_strategy_list_s2 = []
            df_score_s2 = []
            for i, k1 in enumerate(by_field):
                for k2 in by_field[i + 1:]:
                    by_field2 = [k1, k2]
                    df_bwt_strategy_list2, df_strategy_score2 = self.get_cross_strategy(df_test_, by_field2, self.sample_ratio_list,
                                                                                   self.fee_ratio_list, self.report_ratio_list,
                                                                                   self.bad_ratio_interval)
                    df_bwt_strategy_list_s2.extend(df_bwt_strategy_list2)
                    df_score_s2.append(df_strategy_score2)
            df_score_s2 = pd.concat(df_score_s2).reset_index(drop=True).sort_values("赔付率")
            df_bwt_strategy_list_s2 = [df_bwt_strategy_list_s2[i] for i in df_score_s2.index]
            strategy_list.append(df_bwt_strategy_list_s2)
            score_list.append(df_score_s2.reset_index(drop=True))

        if len(by_field) > 2:
            df_bwt_strategy_list_s3 = []
            df_score_s3=[]
            for k3 in by_field:
                by_field3 = [k3] + list(set(by_field) - set([k3]))
                df_bwt_strategy_list3, df_strategy_score3 = self.get_triple_strategy(df_test_, by_field3, self.sample_ratio_list, self.fee_ratio_list,
                                                               self.report_ratio_list, self.bad_ratio_interval)
                if (df_strategy_score3.shape[0]>0) & (len(df_bwt_strategy_list3[0])>0):
                    df_bwt_strategy_list_s3.extend(df_bwt_strategy_list3)
                    df_score_s3.append(df_strategy_score3)

            if len(df_bwt_strategy_list_s3)>0:
                df_score_s3 = pd.concat(df_score_s3).reset_index(drop=True).sort_values("赔付率")
                df_bwt_strategy_list_s3 = [df_bwt_strategy_list_s3[i] for i in df_score_s3.index]
            else:
                df_score_s3 = pd.DataFrame(columns=["通过率", "赔付率", "出险率"])
            strategy_list.append(df_bwt_strategy_list_s3)
            score_list.append(df_score_s3.reset_index(drop=True))


        if dump_path is not None:
            if '.xlsx' == dump_path[:-5]:
                pass
            else:
                dump_path = os.path.join(dump_path,'风控自生成策略_{}_{}.xlsx'.format(report_key,str(datetime.date.today())))
            self.strategy_report.dump_report_2excel(strategy_list, df_test_, topn=report_topn, filePath=dump_path)

        return strategy_list,score_list

class StrategyReport:
    def __init__(self):
        self.INIT_SCORE_STRATEGY = {
            'default': {
                'zj': [
                    {'source': [9, 10], 'target': {'白名单': 10, '灰名单': 6, '黑名单': 3}},
                    {'source': [7, 8], 'target': {'白名单': 9, '灰名单': 6, '黑名单': 3}},
                    {'source': [5, 6], 'target': {'白名单': 8, '灰名单': 5, '黑名单': 2}},
                    {'source': [1, 2, 3, 4], 'target': {'白名单': 7, '灰名单': 4, '黑名单': 1}},
                ],
                'chd': [
                    {'source': [9, 10], 'target': {'白名单': 10, '灰名单': 6, '黑名单': 3}},
                    {'source': [8], 'target': {'白名单': 9, '灰名单': 6, '黑名单': 3}},
                    {'source': [7], 'target': {'白名单': 8, '灰名单': 5, '黑名单': 2}},
                    {'source': [4, 5, 6], 'target': {'白名单': 7, '灰名单': 5, '黑名单': 1}},
                ],
                'card': [
                    {'source': [10], 'target': {'白名单': 10, '灰名单': 10, '黑名单': 10}},
                    {'source': [9], 'target': {'白名单': 9, '灰名单': 9, '黑名单': 9}},
                    {'source': [8], 'target': {'白名单': 8, '灰名单': 8, '黑名单': 8}},
                    {'source': [7], 'target': {'白名单': 7, '灰名单': 7, '黑名单': 7}},
                    {'source': [6], 'target': {'白名单': 6, '灰名单': 6, '黑名单': 6}},
                    {'source': [5], 'target': {'白名单': 5, '灰名单': 5, '黑名单': 5}},
                    {'source': [4], 'target': {'白名单': 4, '灰名单': 4, '黑名单': 4}},
                    {'source': [3], 'target': {'白名单': 3, '灰名单': 3, '黑名单': 3}},
                    {'source': [2], 'target': {'白名单': 2, '灰名单': 2, '黑名单': 2}},
                    {'source': [1], 'target': {'白名单': 1, '灰名单': 1, '黑名单': 1}},
                ],
            },
        }

        self.INIT_SCORE_COLORS = {
            10: '#009fff',
            9: '#009fff',
            8: '#009fff',
            7: '#009fff',
            6: '#ffff00',
            5: '#ffff00',
            4: '#ffff00',
            3: '#ff0000',
            2: '#ff0000',
            1: '#ff0000',
            0: '#808080',
            -1: '#808080',
        }

    def calc_strategy_risk(self,df_tmp_data, by_field):
        df_rep_tmp = df_tmp_data.groupby(by_field).agg(
            {
                'truckno': [('单量', lambda x: len(x)), ('车辆数', lambda x: len(set(x)))],
                'car_got': [("已赚车年", 'sum')],
                'report_num': [("出险次数", 'sum')],
                'report_fee': [("赔付金额", 'sum')],
                'fee_got': [("已赚保费", 'sum')],
            }).droplevel(0, 1).sort_index(ascending=[True, True])
        df_rep_tmp['车辆占比'] = df_rep_tmp['车辆数'] / df_rep_tmp['车辆数'].sum()
        df_rep_tmp['单量占比'] = (df_rep_tmp['单量'] / df_rep_tmp['单量'].sum())
        df_rep_tmp['出险率'] = (df_rep_tmp['出险次数'] / df_rep_tmp['已赚车年']).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['赔付率'] = (df_rep_tmp['赔付金额'] / df_rep_tmp['已赚保费']).apply(lambda x: format(x, '.2%'))

        df_rep_tmp2 = df_rep_tmp[['单量', '单量占比', '出险率', '赔付率']].unstack()
        df_rep_tmp2['单量占比'] = (df_rep_tmp2['单量'] / df_rep_tmp2['单量'].sum(axis=0)).applymap(lambda x: format(x, '.2%'))
        index = df_rep_tmp2.index.sortlevel(level=1, ascending=False)[0]
        columns = df_rep_tmp2.columns.sortlevel(level=1, ascending=False)[0]
        df_rep_out = df_rep_tmp2.loc[index, columns].swaplevel(0, 1, axis=1)
        df_rep_out.index.names = ['g7_tag', 'g7_score']
        return df_rep_out

    def calc_strategy_score(self, df_bwt_strategy):
        func_bwt_code = lambda x: '白名单' if x == 1 else ('黑名单' if x == -1 else '灰名单')
        df_bwt_strategy_name = df_bwt_strategy.applymap(func_bwt_code)
        col_name = df_bwt_strategy.columns.name
        index_name = df_bwt_strategy.index.name
        for score_name in ['zj', 'chd', 'card']:
            if score_name == col_name:
                score_strategy = self.INIT_SCORE_STRATEGY.get('default').get(score_name)
                for strategy_i in score_strategy:
                    source_i = strategy_i.get("source")
                    target_i = strategy_i.get("target")
                    df_bwt_strategy_name.loc[:, source_i] = df_bwt_strategy_name.loc[:, source_i].applymap(
                        lambda x: target_i.get(x, -1))
                break
            if score_name == index_name:
                score_strategy = self.INIT_SCORE_STRATEGY.get('default').get(score_name)
                for strategy_i in score_strategy:
                    source_i = strategy_i.get("source")
                    target_i = strategy_i.get("target")
                    df_bwt_strategy_name.loc[source_i, :] = df_bwt_strategy_name.loc[source_i, :].applymap(
                        lambda x: target_i.get(x, -1))
                break
        return df_bwt_strategy_name

    def calc_single_strategy_report_p1(self, strategy_tmp, df_data):
        return self.calc_cross_strategy_report_p1(strategy_tmp, df_data)

    def calc_cross_strategy_report_p1(self, strategy_tmp, df_data_):
        fields_ = [i for i in [strategy_tmp.index.name, strategy_tmp.columns.name] if i != None]
        df_test_ = df_data_[df_data_[fields_].isna().sum(axis=1) == 0]

        func_bwt_code = lambda x: '白名单' if x == 1 else ('黑名单' if x == -1 else '灰名单')
        df_strategy_tmp = self.calc_strategy_score(strategy_tmp).unstack().to_frame(name='cross_score')
        df_strategy_tmp['cross_tag'] = strategy_tmp.applymap(func_bwt_code).unstack()
        index_shape = len([i for i in df_strategy_tmp.index.names if i != None])
        if index_shape > 1:
            df_test_['cross_idx'] = df_test_[df_strategy_tmp.index.names].fillna(-1).astype(int).apply(
                lambda x: "{}_{}".format(x[0], x[1]), axis=1)
            df_strategy_tmp.index = ['{}_{}'.format(int(i[0]), int(i[1])) for i in df_strategy_tmp.index]
        else:
            df_strategy_tmp.index = df_strategy_tmp.index.droplevel(None)
            df_test_['cross_idx'] = df_test_[df_strategy_tmp.index.names].fillna(-1).astype(int)
            df_strategy_tmp.index = [int(i) for i in df_strategy_tmp.index]
        df_test_ = pd.merge(df_test_, df_strategy_tmp, how='left', left_on='cross_idx', right_index=True)

        df_all = df_test_.copy()
        df_all.company_name = '全量'
        df_sub_company = df_test_.copy()
        df_sub_company["company_name"] = df_sub_company.company_name.apply(lambda x: x[:2])
        sel_company_info = df_sub_company["company_name"].value_counts()
        sel_company = sel_company_info[sel_company_info > 1000].index
        df_sub_company = df_sub_company[df_sub_company.company_name.isin(sel_company)]
        df_tmp_data = pd.concat([df_all, df_sub_company], axis=0)

        df_tmp_data['cross_tmp'] = '汇总'
        df_group_score = self.calc_strategy_risk(df_tmp_data, by_field=['cross_tag', 'cross_score', 'company_name'])
        df_group_tag = self.calc_strategy_risk(df_tmp_data, by_field=['cross_tag', 'cross_tmp', 'company_name'])
        df_group_all = self.calc_strategy_risk(df_tmp_data, by_field=['cross_tmp', 'cross_tmp', 'company_name'])

        df_insu_report = pd.concat([df_group_score, df_group_tag, df_group_all], axis=0)
        tag_weight = {
            '白名单': 50,
            '灰名单': 40,
            '黑名单': 30,
            '汇总': 20
        }
        index_raw = df_insu_report.index
        argsort_index = np.argsort([tag_weight.get(i[0]) + tag_weight.get(i[1], i[1]) * 0.01 for i in index_raw])
        index_ordered = index_raw[argsort_index[::-1]]
        df_insu_report = df_insu_report.loc[index_ordered, :]
        return df_insu_report

    def calc_triple_strategy_report_p1(self, strategy_init, strategy_tmp, df_data_):
        fields_ = [strategy_tmp.index.name, strategy_tmp.columns.name, strategy_init.index.name]
        df_test_ = df_data_[df_data_[fields_].isna().sum(axis=1) == 0]

        strategy_init_tmp = strategy_init[(strategy_init < 0).any(axis=1)].index

        func_bwt_code = lambda x: '白名单' if x == 1 else ('黑名单' if x == -1 else '灰名单')
        df_strategy_tmp = self.calc_strategy_score(strategy_tmp).unstack().to_frame(name='cross_score')
        df_strategy_tmp['cross_tag'] = strategy_tmp.applymap(func_bwt_code).unstack()
        index_shape = len([i for i in df_strategy_tmp.index.names if i != None])
        if index_shape > 1:
            df_test_['cross_idx'] = df_test_[df_strategy_tmp.index.names].fillna(-1).astype(int).apply(
                lambda x: "{}_{}".format(x[0], x[1]), axis=1)
            df_strategy_tmp.index = ['{}_{}'.format(int(i[0]), int(i[1])) for i in df_strategy_tmp.index]
        else:
            df_strategy_tmp.index = df_strategy_tmp.index.droplevel(None)
            df_test_['cross_idx'] = df_test_[df_strategy_tmp.index.names].fillna(-1).astype(int)
            df_strategy_tmp.index = [int(i) for i in df_strategy_tmp.index]
        df_test_ = pd.merge(df_test_, df_strategy_tmp, how='left', left_on='cross_idx', right_index=True)
        # 兜底策略
        df_test_.loc[df_test_[strategy_init_tmp.name].isin(strategy_init_tmp), 'cross_score'] = 1
        df_test_.loc[df_test_[strategy_init_tmp.name].isin(strategy_init_tmp), 'cross_tag'] = '兜底策略'

        df_all = df_test_.copy()
        df_all.company_name = '全量'
        df_sub_company = df_test_.copy()
        df_sub_company["company_name"] = df_sub_company.company_name.apply(lambda x: x[:2])
        sel_company_info = df_sub_company["company_name"].value_counts()
        sel_company = sel_company_info[sel_company_info > 1000].index
        df_sub_company = df_sub_company[df_sub_company.company_name.isin(sel_company)]
        df_tmp_data = pd.concat([df_all, df_sub_company], axis=0)

        df_tmp_data['cross_tmp'] = '汇总'
        df_group_score = self.calc_strategy_risk(df_tmp_data, by_field=['cross_tag', 'cross_score', 'company_name'])
        df_group_tag = self.calc_strategy_risk(df_tmp_data, by_field=['cross_tag', 'cross_tmp', 'company_name'])
        df_group_all = self.calc_strategy_risk(df_tmp_data, by_field=['cross_tmp', 'cross_tmp', 'company_name'])

        df_insu_report = pd.concat([df_group_score, df_group_tag, df_group_all], axis=0)
        tag_weight = {
            '白名单': 50,
            '灰名单': 40,
            '黑名单': 30,
            '兜底策略': 20,
            '汇总': 10
        }
        index_raw = df_insu_report.index
        argsort_index = np.argsort([tag_weight.get(i[0]) + tag_weight.get(i[1], i[1]) * 0.01 for i in index_raw])
        index_ordered = index_raw[argsort_index[::-1]]
        df_insu_report = df_insu_report.loc[index_ordered, :]
        return df_insu_report

    def calc_single_strategy_report_p2(self, strategy_tmp, df_data, table_name):
        strategy_score_tmp = self.calc_strategy_score(strategy_tmp)
        tag_weight = {'汇总': -10}

        def style_apply(content, colors, back_ground=''):
            if content != None and content in colors.keys():
                return 'background-color: ' + colors[content]
            return back_ground

        def style_color(df, colors):
            return df.style.applymap(style_apply, colors=colors)

        df_tmp_data = df_data.copy()
        df_tmp_data['score_tmp'] = '汇总'
        by_field_tmp1 = [strategy_tmp.index.name]
        by_field_tmp2 = ['score_tmp']
        df_list = []
        for by_field_ in [by_field_tmp1, by_field_tmp2]:
            df_rep_tmp = df_tmp_data.groupby(by_field_).agg(
                {
                    'truckno': [('单量', lambda x: len(x)), ('车辆数', lambda x: len(set(x)))],
                    'car_got': [("已赚车年", 'sum')],
                    'report_num': [("出险次数", 'sum')],
                    'report_fee': [("赔付金额", 'sum')],
                    'fee_got': [("已赚保费", 'sum')],
                }).droplevel(0, 1).sort_index(ascending=[True, True])
            df_rep_tmp.index.names = by_field_tmp1
            df_list.append(df_rep_tmp)
        df_rep_tmp = pd.concat(df_list, axis=0)
        df_rep_tmp['单量占比'] = (df_rep_tmp['单量'] / df_rep_tmp['单量'].max()).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['出险率'] = (df_rep_tmp['出险次数'] / df_rep_tmp['已赚车年']).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['赔付率'] = (df_rep_tmp['赔付金额'] / df_rep_tmp['已赚保费']).apply(lambda x: format(x, '.2%'))
        df_rep_out = df_rep_tmp[['单量', '单量占比', '出险率', '赔付率']]

        tag_weight = {
            '赔付率': 60,
            '出险率': 50,
            '单量': 40,
            '单量占比': 30,
            '汇总': -20
        }
        new_index = df_rep_out.index[np.argsort([tag_weight.get(i, i) for i in df_rep_out.index])[::-1]]
        new_col = df_rep_out.columns[np.argsort([tag_weight.get(i) for i in df_rep_out.columns])[::-1]]
        df_rep_out = df_rep_out.loc[new_index, new_col]
        df_rep_out.columns.names = [table_name] + df_rep_out.columns.names[1:]
        if len(df_rep_out.columns.shape) == 1:
            df_rep_out.columns = pd.MultiIndex.from_arrays([len(df_rep_out.columns) * [''], df_rep_out.columns])

        # 颜色格式
        df_rep_out_color = df_rep_out.copy()
        for coli in df_rep_out_color.columns:
            df_tmp_ = df_rep_out_color[coli].apply(lambda x: -1)
            df_tmp_.loc[strategy_score_tmp.index] = strategy_score_tmp.bwl_tag
            df_rep_out_color[coli] = df_tmp_
        style_df = style_color(df_rep_out_color, self.INIT_SCORE_COLORS)
        style_df.render()
        for coli in df_rep_out.columns:
            style_df.data[coli] = df_rep_out[coli].astype(str).values
        style_df
        return style_df

    def calc_cross_strategy_report_p2(self, strategy_tmp, df_data_, table_name):
        fields_ = [strategy_tmp.index.name, strategy_tmp.columns.name]
        df_tmp_data = df_data_[df_data_[fields_].isna().sum(axis=1) == 0]

        strategy_score_tmp = self.calc_strategy_score(strategy_tmp)
        tag_weight = {'汇总': -10}

        def style_apply(content, colors, back_ground=''):
            if content != None and content in colors.keys():
                return 'background-color: ' + colors[content]
            return back_ground

        def style_color(df, colors):
            return df.style.applymap(style_apply, colors=colors)

        df_tmp_data['score_tmp'] = '汇总'
        by_field_tmp1 = [strategy_tmp.index.name, strategy_tmp.columns.name]
        by_field_tmp2 = ['score_tmp', strategy_tmp.columns.name]
        by_field_tmp3 = [strategy_tmp.index.name, 'score_tmp']
        by_field_tmp4 = ['score_tmp', 'score_tmp']
        df_list = []
        for by_field_ in [by_field_tmp1, by_field_tmp2, by_field_tmp3, by_field_tmp4]:
            df_rep_tmp = df_tmp_data.groupby(by_field_).agg(
                {
                    'truckno': [('单量', lambda x: len(x)), ('车辆数', lambda x: len(set(x)))],
                    'car_got': [("已赚车年", 'sum')],
                    'report_num': [("出险次数", 'sum')],
                    'report_fee': [("赔付金额", 'sum')],
                    'fee_got': [("已赚保费", 'sum')],
                }).droplevel(0, 1).sort_index(ascending=[True, True])
            df_rep_tmp.index.names = by_field_tmp1
            df_list.append(df_rep_tmp)
        df_rep_tmp = pd.concat(df_list, axis=0)
        df_rep_tmp['单量占比'] = (df_rep_tmp['单量'] / df_rep_tmp['单量'].max()).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['出险率'] = (df_rep_tmp['出险次数'] / df_rep_tmp['已赚车年']).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['赔付率'] = (df_rep_tmp['赔付金额'] / df_rep_tmp['已赚保费']).apply(lambda x: format(x, '.2%'))
        df_rep_out = df_rep_tmp[['单量', '单量占比', '出险率', '赔付率']].unstack()

        tag_weight = {
            '赔付率': 60,
            '出险率': 50,
            '单量': 40,
            '单量占比': 30,
            '汇总': -20
        }
        new_index = df_rep_out.index[np.argsort([tag_weight.get(i, i) for i in df_rep_out.index])[::-1]]
        new_col = df_rep_out.columns[
            np.argsort([tag_weight.get(i[0]) + tag_weight.get(i[1], i[1]) * 0.01 for i in df_rep_out.columns])[::-1]]
        df_rep_out = df_rep_out.loc[new_index, new_col]
        df_rep_out.columns.names = [table_name] + df_rep_out.columns.names[1:]
        if len(df_rep_out.index.shape) == 1:
            df_rep_out.index = pd.MultiIndex.from_arrays([len(df_rep_out.index) * [''], df_rep_out.index])
        if len(strategy_score_tmp.index.shape) == 1:
            strategy_score_tmp.index = pd.MultiIndex.from_arrays(
                [len(strategy_score_tmp.index) * [''], strategy_score_tmp.index])

        # 颜色格式
        df_rep_out_color = df_rep_out.copy()
        for coli in set([i[0] for i in df_rep_out_color.columns]):
            df_tmp_ = df_rep_out_color[coli].applymap(lambda x: -1)
            df_tmp_.loc[strategy_score_tmp.index, strategy_score_tmp.columns] = strategy_score_tmp
            df_rep_out_color[coli] = df_tmp_
        style_df = style_color(df_rep_out_color.T, self.INIT_SCORE_COLORS)
        style_df.render()
        for coli in set([i[0] for i in df_rep_out.columns]):
            style_df.data.loc[coli, :] = df_rep_out[coli].astype(str).T.values
        return style_df

    def calc_triple_strategy_report_p2(self, strategy_init, strategy_tmp, df_data_, table_name):
        strategy_init_tmp = strategy_init[(strategy_init < 0).any(axis=1)].index
        fields_ = [strategy_tmp.index.name, strategy_tmp.columns.name, strategy_init.index.name]
        strategy_score_tmp = self.calc_strategy_score(strategy_tmp)
        tag_weight = {'汇总': -10}

        def style_apply(content, colors, back_ground=''):
            if content != None and content in colors.keys():
                return 'background-color: ' + colors[content]
            return back_ground

        def style_color(df, colors):
            return df.style.applymap(style_apply, colors=colors)

        df_tmp_data = df_data_[df_data_[fields_].isna().sum(axis=1) == 0]
        df_tmp_data_sub1 = df_tmp_data.loc[df_tmp_data[strategy_init_tmp.name].isin(strategy_init_tmp)]
        df_tmp_data_sub1.loc[
            df_tmp_data[strategy_init_tmp.name].isin(strategy_init_tmp), strategy_tmp.index.name] = '兜底策略'
        df_tmp_data_sub2 = df_tmp_data.loc[df_tmp_data[strategy_init_tmp.name].isin(strategy_init_tmp)]
        df_tmp_data_sub2.loc[
            df_tmp_data[strategy_init_tmp.name].isin(strategy_init_tmp), strategy_tmp.columns.name] = '兜底策略'

        df_tmp_data['score_tmp'] = '汇总'
        by_field_tmp1 = [strategy_tmp.index.name, strategy_tmp.columns.name]
        df_tmp_data2 = pd.concat([df_tmp_data, df_tmp_data_sub1, df_tmp_data_sub2], axis=0)
        df_rep_tmpi = df_tmp_data2.groupby(by_field_tmp1).agg(
            {
                'truckno': [('单量', lambda x: len(x)), ('车辆数', lambda x: len(set(x)))],
                'car_got': [("已赚车年", 'sum')],
                'report_num': [("出险次数", 'sum')],
                'report_fee': [("赔付金额", 'sum')],
                'fee_got': [("已赚保费", 'sum')],
            }).droplevel(0, 1).sort_index(ascending=[True, True])
        df_rep_tmpi.index.names = by_field_tmp1
        df_list = [df_rep_tmpi]

        by_field_tmp2 = ['score_tmp', strategy_tmp.columns.name]
        by_field_tmp3 = [strategy_tmp.index.name, 'score_tmp']
        by_field_tmp4 = ['score_tmp', 'score_tmp']
        df_tmp_data.loc[df_tmp_data[strategy_init_tmp.name].isin(strategy_init_tmp), strategy_tmp.index.name] = '兜底策略'
        df_tmp_data.loc[df_tmp_data[strategy_init_tmp.name].isin(strategy_init_tmp), strategy_tmp.columns.name] = '兜底策略'
        for by_field_ in [by_field_tmp2, by_field_tmp3, by_field_tmp4]:
            df_rep_tmpi = df_tmp_data.groupby(by_field_).agg(
                {
                    'truckno': [('单量', lambda x: len(x)), ('车辆数', lambda x: len(set(x)))],
                    'car_got': [("已赚车年", 'sum')],
                    'report_num': [("出险次数", 'sum')],
                    'report_fee': [("赔付金额", 'sum')],
                    'fee_got': [("已赚保费", 'sum')],
                }).droplevel(0, 1).sort_index(ascending=[True, True])
            df_rep_tmpi.index.names = by_field_tmp1
            df_list.append(df_rep_tmpi)

        df_rep_tmp = pd.concat(df_list, axis=0)
        df_rep_tmp['单量占比'] = (df_rep_tmp['单量'] / df_rep_tmp['单量'].max()).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['出险率'] = (df_rep_tmp['出险次数'] / df_rep_tmp['已赚车年']).apply(lambda x: format(x, '.2%'))
        df_rep_tmp['赔付率'] = (df_rep_tmp['赔付金额'] / df_rep_tmp['已赚保费']).apply(lambda x: format(x, '.2%'))
        df_rep_out = df_rep_tmp[['单量', '单量占比', '出险率', '赔付率']].unstack()

        tag_weight = {
            '赔付率': 60,
            '出险率': 50,
            '单量': 40,
            '单量占比': 30,
            '兜底策略': -10,
            '汇总': -20
        }
        new_index = df_rep_out.index[np.argsort([tag_weight.get(i, i) for i in df_rep_out.index])[::-1]]
        new_col = df_rep_out.columns[
            np.argsort([tag_weight.get(i[0]) + tag_weight.get(i[1], i[1]) * 0.01 for i in df_rep_out.columns])[::-1]]
        df_rep_out = df_rep_out.loc[new_index, new_col]
        df_rep_out.columns.names = [table_name] + df_rep_out.columns.names[1:]
        if len(df_rep_out.index.shape) == 1:
            df_rep_out.index = pd.MultiIndex.from_arrays([len(df_rep_out.index) * [''], df_rep_out.index])
        if len(strategy_score_tmp.index.shape) == 1:
            strategy_score_tmp.index = pd.MultiIndex.from_arrays(
                [len(strategy_score_tmp.index) * [''], strategy_score_tmp.index])

        # 颜色格式
        df_rep_out_color = df_rep_out.copy()
        for coli in set([i[0] for i in df_rep_out_color.columns]):
            df_tmp_ = df_rep_out_color[coli].applymap(lambda x: -1)
            df_tmp_.loc[strategy_score_tmp.index, strategy_score_tmp.columns] = strategy_score_tmp
            df_tmp_.loc['兜底策略', :-1] = 1
            df_tmp_.loc[:-1, '兜底策略'] = 1
            df_rep_out_color[coli] = df_tmp_
        style_df = style_color(df_rep_out_color.T, self.INIT_SCORE_COLORS)
        style_df.render()
        for coli in set([i[0] for i in df_rep_out.columns]):
            style_df.data.loc[coli, :] = df_rep_out[coli].astype(str).T.values
        return style_df

    def get_single_strategy_report(self, strategy_tmp, df_test):
        df_report_list = []
        df_insu_report = self.calc_single_strategy_report_p1(strategy_tmp, df_test)
        df_report_list.append(df_insu_report)
        df_sub_report = self.calc_single_strategy_report_p2(strategy_tmp, df_test, '全量(全保司)')
        df_report_list.append(df_sub_report)
        for sub_company in set([i[0] for i in df_insu_report.columns]):
            df_test_sub = df_test[df_test.company_name.apply(lambda x: x[:2] == sub_company)]
            if df_test_sub.shape[0] < 1000:
                continue
            df_sub_reporti = self.calc_single_strategy_report_p2(strategy_tmp, df_test_sub, sub_company)
            df_report_list.append(df_sub_reporti)
        return df_report_list

    def get_cross_strategy_report(self, strategy_tmp, df_test):
        df_report_list = []
        df_insu_report = self.calc_cross_strategy_report_p1(strategy_tmp, df_test)
        df_report_list.append(df_insu_report)
        df_sub_report = self.calc_cross_strategy_report_p2(strategy_tmp, df_test, '全量(全保司)')
        df_report_list.append(df_sub_report)
        for sub_company in set([i[0] for i in df_insu_report.columns]):
            df_test_sub = df_test[df_test.company_name.apply(lambda x: x[:2] == sub_company)]
            if df_test_sub.shape[0] < 1000:
                continue
            df_sub_reporti = self.calc_cross_strategy_report_p2(strategy_tmp, df_test_sub, sub_company)
            df_report_list.append(df_sub_reporti)
        return df_report_list

    def get_triple_strategy_report(self, strategy_init, strategy_tmp, df_data_):
        fields_ = [strategy_tmp.index.name, strategy_tmp.columns.name, strategy_init.index.name]
        df_test = df_data_[df_data_[fields_].isna().sum(axis=1) == 0]
        df_report_list = []
        df_insu_report = self.calc_triple_strategy_report_p1(strategy_init, strategy_tmp, df_test)
        df_report_list.append(df_insu_report)
        df_init_report = self.calc_single_strategy_report_p2(strategy_init, df_test, '兜底策略')
        df_report_list.append(df_init_report)
        df_sub_report = self.calc_triple_strategy_report_p2(strategy_init, strategy_tmp, df_test, '全量(全保司)')
        df_report_list.append(df_sub_report)
        for sub_company in set([i[0] for i in df_insu_report.columns]):
            df_test_sub = df_test[df_test.company_name.apply(lambda x: x[:2] == sub_company)]
            if df_test_sub.shape[0] < 1000:
                continue
            df_sub_reporti = self.calc_triple_strategy_report_p2(strategy_init, strategy_tmp, df_test_sub, sub_company)
            df_report_list.append(df_sub_reporti)
        return df_report_list

    def dump_report_2excel(self, strategy_set_, df_test_, topn=50,filePath='风控自生成策略.xlsx'):
        if len(strategy_set_)==1:
            topn_list=[topn]
        elif len(strategy_set_)==2:
            strategy_single_num = min(topn * 0.3, len(strategy_set_[0]))
            strategy_cross_num = min(topn - strategy_single_num,len(strategy_set_[1]))
            topn_list = [int(strategy_single_num),int(strategy_cross_num)]
        else:
            strategy_triple_num = min(topn * 0.2,len(strategy_set_[2]))
            strategy_single_num = min(topn * 0.3 - strategy_triple_num, len(strategy_set_[0]))
            strategy_cross_num = min(topn - strategy_triple_num - strategy_single_num, len(strategy_set_[1]))
            topn_list = [int(strategy_single_num), int(strategy_cross_num),int(strategy_triple_num)]

        writer = pd.ExcelWriter(filePath, engine='openpyxl')
        pd.DataFrame().to_excel(writer, sheet_name='风控方案汇总')

        def get_triple_strategy_tmp(strategy_tmp, df_data_):
            return self.get_triple_strategy_report(strategy_tmp[0], strategy_tmp[1], df_data_)

        func_strategy_report_list = [self.get_single_strategy_report, self.get_cross_strategy_report,
                                     get_triple_strategy_tmp]
        df_report_sum = [pd.DataFrame()]
        for i, strategy_list in enumerate(strategy_set_):
            get_strategy_sheet_report = func_strategy_report_list[i]
            for j, strategy_tmp in enumerate(strategy_list[:topn_list[i]]):
                report_list = get_strategy_sheet_report(strategy_tmp, df_test_)
                if ('白名单', '汇总') not in report_list[0].index:
                    continue
                currow = 1
                sheet_name = '方案{}_T{}'.format(i + 1, j + 1)
                pd.DataFrame(['=HYPERLINK("#风控方案汇总!B2","主目录")']).to_excel(writer, startrow=0, startcol=0, index=False,
                                                                          header=False, sheet_name=sheet_name)
                for report_i in report_list:
                    report_i.to_excel(writer, startrow=currow, startcol=1, index=True, header=True,
                                      sheet_name=sheet_name)
                    if isinstance(report_i, pd.io.formats.style.Styler):
                        currow = currow + report_i.data.shape[0] + 5
                    else:
                        currow = currow + report_i.shape[0] + 7
                report_sumi = report_list[0].loc[[('白名单', '汇总')], :].head(1)
                report_sumi.reset_index(drop=True, inplace=True)
                sheet_index = '=HYPERLINK("#{}!B2","{}")'.format(sheet_name, sheet_name)
                report_sumi.index = [sheet_index]
                df_report_sum.append(report_sumi)
        pd.concat(df_report_sum).to_excel(writer, startrow=1, startcol=1, sheet_name='风控方案汇总')
        writer.save()
        writer.close()
