# -*- coding: utf-8 -*-
# /usr/bin/env python

'''
Author: wenqiangw
Email: wqwangchn@163.com
Date: 2022/4/20 11:31
Desc:
'''
from xgboost import XGBClassifier
import pandas as pd

df_valid = pd.read_csv("../score_ecard/data/train_test_data.csv")
df_train_data = df_valid[df_valid['train_test_tag'] == '训练集'].fillna(0).head(10000)
df_test_data = df_valid[df_valid['train_test_tag'] == '测试集'].fillna(0).head(10000)
feature_columns = df_train_data.columns[4:33].tolist()
feature_columns.extend(df_train_data.columns[36:46])
df_X = df_train_data[feature_columns]
# df_Y = df_train_data['label']
df_Y=df_train_data.apply(lambda x:x['label'] if x["report_fee"]<5000 else 2,axis=1)

params_xgb = {
            'n_estimators': 3,
            'max_depth':3,
            'eta': 0.3,
            'min_child_weight': 1,
            'gamma': 0.3,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'booster': 'gbtree',
            'objective': 'binary:logistic',
            'scale_pos_weight': 1,
            'lambda': 1,
            'seed':666,
            'silent': 0,
            'eval_metric': 'auc'
        }
clf_xgb = XGBClassifier(**params_xgb)
clf_xgb.fit(df_X, df_Y)
aa=clf_xgb.get_booster()
aa.trees_to_dataframe()


def get_insurance_strategy_data(df_report_test, sample_ratio_list, fee_ratio_list, report_ratio_list):
    '''

    :param df_report_test: 评分分档赔付数据
    :param sample_ratio_list: 样本通过率 eg:[60%，65%]
    :param fee_ratio_list: 赔付率 eg:[60%，65%]
    :param report_ratio_list: 出险率 eg:[60%，65%]
    :return:
    '''
    assert len(sample_ratio_list) > 0
    assert len(fee_ratio_list)+len(report_ratio_list) > 0
    if len(fee_ratio_list)<1:
        fee_ratio_list = [1e6]
    if len(report_ratio_list)<1:
        report_ratio_list = [1e6]

    strategy_data = []
    for sample_ratio in sample_ratio_list:
        for fee_ratio in fee_ratio_list:
            for report_ratio in report_ratio_list:
                idx1 = df_report_test.样本占比 >= sample_ratio
                idx2 = df_report_test.出险率 <= report_ratio
                idx3 = df_report_test.赔付率 <= fee_ratio
                idata = df_report_test[idx1 & idx2 & idx3]
                strategy_data.append(idata)

    df_strategy = pd.concat(strategy_data,axis=0).drop_duplicates()

    return df_strategy
