import pymysql
import csv
from cnx_information import BaseManager
from pymysql.cursors import DictCursor
from datetime import datetime, date
import pandas as pd
import numpy as np
import pprint
import xlrd  # 엑셀파일 읽어올 때
import csv  # csv파일 읽어올 때
import traceback   # error 메세지 적을 때
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')


class Worker(BaseManager):
    def __init__(self):
        self.dbname = 'nas'

    def sample_analysis(self):
        sql = "SELECT * FROM regular_season_batter"

        # db 연결
        try:
            cnx_db = self.get_cnx(self.dbname, cursorclass=DictCursor, autocommit=False)
            cur_db = cnx_db.cursor()
            print('SUCCESS DB CONNECT')
        except:
            print(traceback.format_exc())
            return Worker

        # # DB를 dictionary로 읽어오기
        # cur_db.execute(sql)
        # regular_rows = cur_db.fetchall()

        # DB를 바로 dataframe으로 읽어오기
        self.regular = pd.read_sql(sql, cnx_db)
        print(self.regular.columns)

        # # plotting seaborn distplot
        # sns.distplot(regular['year'])
        # plt.show()
        # sns.distplot(regular['AB'])
        # plt.show()

        # # summary statistics
        # print(regular['year'].describe())
        #
        # # groupby position mean
        # print(regular.groupby('position')['OPS'].mean())
        # print(regular.groupby('handed')['OPS'].mean())
        #
        # # position 별 factorplot
        #     # 101명이 position이 ''(공백)으로 나오는데 왜 그런지는 모르겠음.
        # plt.rc('font', family='Malgun Gothic')
        # a = sns.factorplot('position', 'OPS', data=regular, size=4, aspect=2)
        # a.set_xticklabels(rotation=90)
        # plt.show()

    # 운과 실력 구분하기
    def get_self_corr(self, var):

        # # db 연결
        # try:
        #     cnx_db = self.get_cnx(self.dbname, cursorclass=DictCursor, autocommit=False)
        #     cur_db = cnx_db.cursor()
        #     print('SUCCESS DB CONNECT')
        # except:
        #     print(traceback.format_exc())
        #     return Worker
        #
        # # # DB를 dictionary로 읽어오기
        # # cur_db.execute(sql)
        # # regular_rows = cur_db.fetchall()
        #
        # # DB를 바로 dataframe으로 읽어오기
        # self.regular = pd.read_sql(sql, cnx_db)
        # print(self.regular.columns)

        x = []
        y = []
        regular1 = self.regular.loc[self.regular['AB'] >= 50, ]  # 50경기 이상인 사람만
        for name in regular1['batter_name'].unique():
            a = regular1[['batter_name']==name, ].sort_value('year')  # year에 따라 sort
            k = []
            for i in a['year'].unique():
                if (a['year'] == i+1).sum() == 1:
                    k.append(i)
            for i in k:
                x.append(a.loc[a['year']==i, var].iloc[0])
                y.append(a.loc[a['year']==i+1, var].iloc[0])
        plt.scatter(x, y)
        plt.title(var)
        plt.show()
        print(pd.Series(x).corr(pd.Series(y))**2)
        self.regular['H_1B']=self.regular['H']-self.regular['H_2B']-self.regular['H_3B']-self.regular['HR']


# Worker().sample_analysis()
Worker().get_self_corr()

