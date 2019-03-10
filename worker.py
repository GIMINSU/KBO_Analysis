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

from config import config

class Worker(BaseManager):
    def __init__(self):
        self.dbname = 'nas'

    def make_data(self):
        # db연결
        try:
            cnx_db = self.get_cnx(self.dbname, cursorclass=DictCursor, autocommit=False)
            cur_db = cnx_db.cursor()
            print("SUCCESS DB Connect")
        except:
            print("ERROR_DB_Connect")

        insert_dict = dict()
        # csv 파일 읽어오기
        with open('C:/Users/is/Desktop/Pre_Season_Batter.csv', encoding='UTF8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row['height_weight']) > 10:
                    weight=row['height_weight'][-5:-2]
                elif len(row['height_weight']) == 10:
                    weight = row['height_weight'][-4:-2]

                born_date = "".join(filter(str.isdigit, row['year_born']))

                starting_salary = "".join(filter(str.isdigit, row['starting_salary']))

                if row['batter_id'] not in insert_dict:
                    insert_dict[row['batter_id']] = dict()
                if row['year'] not in insert_dict[row['batter_id']]:
                    insert_dict[row['batter_id']][row['year']] = dict()
                if row['batter_id'] in insert_dict:
                    if row['year'] in insert_dict[row['batter_id']]:
                        insert_dict[row['batter_id']][row['year']] = dict(
                            batter_name=row['batter_name'],
                            team=row['team'],
                            avg=row['avg'],
                            G=row['G'],
                            AB=row['AB'],
                            R=row['R'],
                            H=row['H'],
                            H_2B=row['2B'],
                            H_3B=row['3B'],
                            HR=row['HR'],
                            TB=row['TB'],
                            RBI=row['RBI'],
                            SB=row['SB'],
                            CS=row['CS'],
                            BB=row['BB'],
                            HBP=row['HBP'],
                            SO=row['SO'],
                            GDP=row['GDP'],
                            SLG=row['SLG'],
                            OBP=row['OBP'],
                            E=row['E'],
                            height=row['height_weight'][0:3],
                            weight=weight,
                            born_date=born_date,
                            position=row['position'],
                            career=row['career'],
                            starting_salary=starting_salary,
                            OPS=row['OPS']
                        )

        # pprint.pprint(insert_dict)

        #     line_count = 0
        #     for row in csv_reader:
        #         if line_count == 0:
        #             for i in range(len(row)):
        #                 if row[i] not in insert_data:
        #                     insert_data[row[i]]=[]
        #     # print(insert_data.keys())
        #         # if line_count != 0:
        #         #     # for i in range(len(row)):
        #         #     print(row[0])
        #         #         # insert_data[row[i]].append(row[i])
        #         if line_count != 0:
        #             insert_data['batter_id'].append(row[0])
        #             insert_data['batter_name'].append(row[1])
        #             insert_data['year'].append(row[2])
        #             insert_data['team'].append(row[3])
        #             insert_data['avg'].append(row[4])
        #             insert_data['G'].append(row[5])
        #             insert_data['AB'].append(row[6])
        #             insert_data['R'].append(row[7])
        #             insert_data['H'].append(row[8])
        #             insert_data['2B'].append(row[9])
        #             insert_data['3B'].append(row[10])
        #             insert_data['HR'].append(row[11])
        #             insert_data['TB'].append(row[12])
        #             insert_data['RBI'].append(row[13])
        #             insert_data['SB'].append(row[14])
        #             insert_data['CS'].append(row[15])
        #             insert_data['BB'].append(row[16])
        #             insert_data['HBP'].append(row[17])
        #             insert_data['SO'].append(row[18])
        #             insert_data['GDP'].append(row[19])
        #             insert_data['SLG'].append(row[20])
        #             insert_data['OBP'].append(row[21])
        #             insert_data['E'].append(row[22])
        #             insert_data['height_weight'].append(row[23])
        #             insert_data['year_born'].append(row[24])
        #             insert_data['position'].append(row[25])
        #             insert_data['career'].append(row[26])
        #             insert_data['starting_salary'].append(row[27])
        #             insert_data['OPS'].append(row[28])
        #
        #
        #         line_count += 1
        #
        # print(insert_data)

        # for row in insert_data:
        #     print(row)
        # create_table_name = "Pre_Season_Batter"
        # sql_create = """
        # CREATE TABLE IF NOT EXISTS `{}` (
        # `batter_id` INT(11) NOT NULL,
        # `batter_name` VARCHAR(50) COLLATE utf8_general_ci NOT NULL,
        # `year`  YEAR(4) NOT NULL,
        # `team` VARCHAR(50) COLLATE utf8_general_ci DEFAULT NULL,
        # `avg` FLOAT DEFAULT NULL,
        # `G` INT(11) DEFAULT NULL,
        # `AB` INT(11) DEFAULT NULL,
        # `R` INT(11) DEFAULT NULL,
        # `H` INT(11) DEFAULT NULL,
        # `2B` INT(11) DEFAULT NULL,
        # `3B` INT(11) DEFAULT NULL,
        # `HR` INT(11) DEFAULT NULL,
        # `TB` INT(11) DEFAULT NULL,
        # `RBI` INT(11) DEFAULT NULL,
        # `SB` INT(11) DEFAULT NULL,
        # `CS` INT(11) DEFAULT NULL,
        # `BB` INT(11) DEFAULT NULL,
        # `HBP` INT(11) DEFAULT NULL,
        # `SO` INT(11) DEFAULT NULL,
        # `GDP` INT(11) DEFAULT NULL,
        # `SLG` FLOAT DEFAULT NULL,
        # `OBP` FLOAT DEFAULT NULL,
        # `height_weight` VARCHAR(50) COLLATE utf8_general_ci DEFAULT NULL,
        # `position` VARCHAR(50) COLLATE utf8_general_ci DEFAULT NULL,
        # `career` VARCHAR(150) COLLATE utf8_general_ci DEFAULT NULL,
        # `starting_salary` VARCHAR(20) COLLATE utf8_general_ci DEFAULT NULL,
        # `OPS` FLOAT DEFAULT NULL,
        # PRIMARY KEY(`batter_id`),
        # key `IDX_batter_name` (`batter_name`),
        # key `IDX_year` (`year`)
        # ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
        # """.format(create_table_name)
        #
        # try:
        #     cur_db.execute(sql_create)
        #     cnx_db.commit()
        # except:
        #     print(traceback.format_exc())
        #
        # sql_ins = """
        # INSERT INTO {} (batter_id, batter_name, year, team, avg, G, AB, R, H, 2B, 3B, HR, TB, RBI,
        # SB, CS, BB, HBP, SO, GDP, SLG, OBP, height_weight, position, career, starting_salary, OPS)
        # VAULES
        # (%(batter_id)s, %(batter_name)s, %(year)s, %(team)s, %(avg)s, %(G)s, %(AB)s, %(R)s, %(H)s,
        # %(2B)s, %(3B)s, %(HR)s, %(TB)s, %(RBI)s, %(SB)s, %(CS)s, %(BB)s, %(HBP)s, %(SO)s, %(GDP)s,
        # %(SLG)s, %(OBP)s, %(height_weight)s, %(position)s, %(career)s, %(starting_salary)s, %(OPS)s)
        # """.format(create_table_name)
        #
        # idata = []
        # for
        # try:
        #     cur_db.executemany(sql_ins, idata)
        #     cnx_db.commit()
        # except:
        #     print(traceback.format_exc())

Worker().make_data()
