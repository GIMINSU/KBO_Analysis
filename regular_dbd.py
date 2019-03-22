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

class Worker(BaseManager):
    def __init__(self):
        self.dbname = 'nas'

    def make_data(self):

        # db 연결
        try:
            cnx_db = self.get_cnx(self.dbname, cursorclass=DictCursor, autocommit=False)
            cur_db = cnx_db.cursor()
            print('SUCCESS DB CONNECT')
        except:
            print(traceback.format_exc())

        # variable_list 만들기
        variable_list = []
        with open('C:/Users/senti/Desktop/Regular_Season_Batter_Day_by_Day.csv', encoding='UTF8') as csv_file:
            csv_rows = csv.reader(csv_file, delimiter=',')
            linecount = 0
            for row in csv_rows:
                if linecount == 0:
                    variable_list = row
                    linecount += 1

        # for i in range(len(variable_list)):
        #     if variable_list[i] == '2B':
        #         variable_list[i] = 'H_2B'
        #     if variable_list[i] == '3B':
        #         variable_list[i] = 'H_3B'
        variable_list.remove('date')
        variable_list.append('month')
        variable_list.append('day')
        print(variable_list)

        # insert_data 만들기
        insert_dict = dict()
        with open('C:/Users/senti/Desktop/Regular_Season_Batter_Day_by_Day.csv', encoding='UTF8') as csv_file:
            csv_rows = csv.DictReader(csv_file, delimiter=',')
            for row in csv_rows:
                batter_id = row['batter_id']
                if row['date'] == '' or row['date'] == '-':
                    row['date'] = None
                month = int(row['date'].split(".")[0])
                day = int(row['date'].split(".")[1])
                year = row['year']
                if row['date'] is not None:
                    if batter_id not in insert_dict:
                        insert_dict[batter_id] = dict()
                    if year not in insert_dict[batter_id]:
                        insert_dict[batter_id][year] = dict()
                    if month not in insert_dict[batter_id][year]:
                        insert_dict[batter_id][year][month] = dict()
                    if day not in insert_dict[batter_id][year][month]:
                        insert_dict[batter_id][year][month][day] = dict()

                    for variable in variable_list:
                        if variable != 'month' and variable != 'day':
                            if row[variable] == '' or row[variable] == '-':
                                row[variable] = None
                            if variable not in insert_dict[batter_id][year][month][day]:
                                insert_dict[batter_id][year][month][day][variable] = None
                            if variable in insert_dict[batter_id][year][month][day]:
                                insert_dict[batter_id][year][month][day][variable] = row[variable]
                                # print(insert_dict)
        # pprint.pprint(insert_dict)

        create_table_name = "Regular_Season_Batter_Day_by_Day"
        sql_create = """
        CREATE TABLE IF NOT EXISTS `{}` (
        `batter_id` VARCHAR(11) NOT NULL,
        `batter_name` VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `year` YEAR(4) NOT NULL,
        `month` INT(11) NOT NULL,
        `day` INT(11) NOT NULL,
        `opposing_team` VARCHAR(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
        `avg1` FLOAT DEFAULT NULL,
        `avg2` FLOAT DEFAULT NULL,
        `AB` INT(11) DEFAULT NULL,
        `R` INT(11) DEFAULT NULL,
        `H` INT(11) DEFAULT NULL,
        `H_2B` INT(11) DEFAULT NULL,
        `H_3B` INT(11) DEFAULT NULL,
        `HR` INT(11) DEFAULT NULL,
        `RBI` INT(11) DEFAULT NULL,
        `SB` INT(11) DEFAULT NULL,
        `CS` INT(11) DEFAULT NULL,
        `BB` INT(11) DEFAULT NULL,
        `HBP` INT(11) DEFAULT NULL,
        `SO` INT(11) DEFAULT NULL,
        `GDP` FLOAT DEFAULT NULL
        ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """.format(create_table_name)

        # sql_create = """
        #        CREATE TABLE IF NOT EXISTS `{}` (
        #        `batter_id` int(11) NOT NULL,
        #        `year` int(4) NOT NULL,
        #        `month` INT(11) NOT NULL,
        #        `day` INT(11) NOT NULL
        #        ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        #        """.format(create_table_name)

        cur_db.execute(sql_create)
        cnx_db.commit()

        sql_ins = """
        INSERT INTO {} (batter_id, batter_name, year, month, day, opposing_team, avg1, avg2, AB, R, H, H_2B, H_3B, HR, RBI, SB, CS, BB, HBP, SO, GDP)
        VALUES
        (%(batter_id)s, %(batter_name)s, %(year)s, %(month)s, %(day)s, %(opposing_team)s, %(avg1)s, %(avg2)s, %(AB)s, %(R)s, %(H)s, %(H_2B)s, %(H_3B)s, %(HR)s, %(RBI)s, %(SB)s, %(CS)s, %(BB)s, %(HBP)s, %(SO)s, %(GDP)s)
        """.format(create_table_name)

        idata = []
        for batter_id in insert_dict:
            for year in insert_dict[batter_id]:
                for month in insert_dict[batter_id][year]:
                    for day in insert_dict[batter_id][year][month]:
                        idata.append(dict(
                            batter_id=batter_id,
                            batter_name=insert_dict[batter_id][year][month][day]['batter_name'],
                            year=year,
                            month=month,
                            day=day,
                            opposing_team=insert_dict[batter_id][year][month][day]['opposing_team'],
                            avg1=insert_dict[batter_id][year][month][day]['avg1'],
                            avg2=insert_dict[batter_id][year][month][day]['avg2'],
                            AB=insert_dict[batter_id][year][month][day]['AB'],
                            R=insert_dict[batter_id][year][month][day]['R'],
                            H=insert_dict[batter_id][year][month][day]['H'],
                            H_2B=insert_dict[batter_id][year][month][day]['2B'],
                            H_3B=insert_dict[batter_id][year][month][day]['3B'],
                            HR=insert_dict[batter_id][year][month][day]['HR'],
                            RBI=insert_dict[batter_id][year][month][day]['RBI'],
                            SB=insert_dict[batter_id][year][month][day]['SB'],
                            CS=insert_dict[batter_id][year][month][day]['CS'],
                            BB=insert_dict[batter_id][year][month][day]['BB'],
                            HBP=insert_dict[batter_id][year][month][day]['HBP'],
                            SO=insert_dict[batter_id][year][month][day]['SO'],
                            GDP=insert_dict[batter_id][year][month][day]['GDP']
                        ))
        # sql_ins = """
        #         INSERT INTO {} (batter_id, year, month, day)
        #         VALUES
        #         (%(batter_id)s, %(year)s, %(month)s, %(day)s)
        #         """.format(create_table_name)
        #
        # idata = []
        # for batter_id in insert_dict:
        #     for year in insert_dict[batter_id]:
        #         for month in insert_dict[batter_id][year]:
        #             for day in insert_dict[batter_id][year][month]:
        #                 idata.append(dict(
        #                     batter_id=batter_id,
        #                     year=year,
        #                     month=month,
        #                     day=day,
        #                     # oppsing_team=insert_dict[batter_id][year][month][day]['opposing_team']
        #                     # avg1=insert_dict[batter_id][year][month][day]['avg1']
        #                     # avg2=insert_dict[batter_id][year][month][day]['avg2']
        #                 ))
        try:
            cur_db.executemany(sql_ins, idata)
            cnx_db.commit()
        except:
            print(traceback.format_exc())

Worker().make_data()