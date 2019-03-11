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
        # db연결
        try:
            cnx_db = self.get_cnx(self.dbname, cursorclass=DictCursor, autocommit=False)
            cur_db = cnx_db.cursor()
            print("SUCCESS DB Connect")
        except:
            print("ERROR_DB_Connect")

        insert_dict = dict()
        variables_list = []
        filter_variable_list = []
        weight = 0
        born_date = 0
        # csv 파일 읽어오기
        with open('C:/Users/senti/Desktop/Pre_Season_Batter.csv', encoding='UTF8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            linecount = 0
            # print(csv_reader)
            for row in csv_reader:
                if linecount == 0:
                    variables_list = row
                    linecount += 1

        # print(variables_list)

        with open('C:/Users/senti/Desktop/Pre_Season_Batter.csv', encoding='UTF8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                for variable in variables_list:
                    if row[variable] == '' or row[variable] == '-':
                        if variable not in filter_variable_list:
                            filter_variable_list.append(variable)
        # print(filter_variable_list)
        #         # print(row)

                if len(row['height/weight']) > 10:
                    weight = row['height/weight'][-5:-2]
                elif len(row['height/weight']) == 10:
                    weight = row['height/weight'][-4:-2]

                born_date = "".join(filter(str.isdigit, row['year_born']))

                starting_salary = "".join(filter(str.isdigit, row['starting_salary']))
                if row['batter_id'] not in insert_dict:
                    insert_dict[row['batter_id']] = dict()

                if row['batter_id'] not in insert_dict:
                    insert_dict[row['batter_id']] = dict()
                if row['year'] not in insert_dict[row['batter_id']]:
                    insert_dict[row['batter_id']][row['year']] = dict(
                        batter_name=None,
                        team=None,
                        avg=None,
                        G=None,
                        AB=None,
                        R=None,
                        H=None,
                        H_2B=None,
                        H_3B=None,
                        HR=None,
                        TB=None,
                        RBI=None,
                        SB=None,
                        CS=None,
                        BB=None,
                        HBP=None,
                        SO=None,
                        GDP=None,
                        SLG=None,
                        OBP=None,
                        E=None,
                        height=None,
                        weight=None,
                        born_date=None,
                        position=None,
                        career=None,
                        starting_salary=None,
                        OPS=None
                    )

                for variable in variables_list:
                    if variable not in filter_variable_list:
                        if variable != 'year_born' or variable == 'height/weight':
                            insert_dict[row['batter_id']][row['year']][variable] = row[variable]
                        if variable == 'height/weight':
                            insert_dict[row['batter_id']][row['year']]['height'] = row[variable][0:3]
                            insert_dict[row['batter_id']][row['year']]['weight'] = weight
                        if variable == 'year_born':
                            insert_dict[row['batter_id']][row['year']]['born_date'] = born_date
                    if variable in filter_variable_list:
                        if row[variable] != '' and row[variable] != '-':
                            if variable != 'starting_salary':
                                insert_dict[row['batter_id']][row['year']][variable] = row[variable]
                            if variable == 'starting_salary':
                                insert_dict[row['batter_id']][row['year']][variable] = starting_salary


        #         if row['year'] not in insert_dict[row['batter_id']]:
        #             insert_dict[row['batter_id']][row['year']] = dict(
        #                 batter_name=None,
        #                 team=None,
        #                 avg=None,
        #                 G=None,
        #                 AB=None,
        #                 R=None,
        #                 H=None,
        #                 H_2B=None,
        #                 H_3B=None,
        #                 HR=None,
        #                 TB=None,
        #                 RBI=None,
        #                 SB=None,
        #                 CS=None,
        #                 BB=None,
        #                 HBP=None,
        #                 SO=None,
        #                 GDP=None,
        #                 SLG=None,
        #                 OBP=None,
        #                 E=None,
        #                 height=None,
        #                 weight=None,
        #                 born_date=None,
        #                 position=None,
        #                 career=None,
        #                 starting_salary=None,
        #                 OPS=None
        #             )
        #         if row['batter_id'] in insert_dict:
        #             if row['year'] in insert_dict[row['batter_id']]:
        #                 if row['avg'] != '-' or row['avg'] != '':
        #                     insert_dict[row['batter_id']][row['year']]['avg'] = float(row['avg'])
        #                 if row['']
        #                 insert_dict[row['batter_id']][row['year']] = dict(
        #                     batter_name=str(row['batter_name']),
        #                     team=str(row['team']),
        #                     avg=float(row['avg']),
        #                     G=row['G'],
        #                     AB=row['AB'],
        #                     R=row['R'],
        #                     H=row['H'],
        #                     H_2B=row['2B'],
        #                     H_3B=row['3B'],
        #                     HR=row['HR'],
        #                     TB=row['TB'],
        #                     RBI=row['RBI'],
        #                     SB=row['SB'],
        #                     CS=row['CS'],
        #                     BB=row['BB'],
        #                     HBP=row['HBP'],
        #                     SO=row['SO'],
        #                     GDP=row['GDP'],
        #                     SLG=row['SLG'],
        #                     OBP=row['OBP'],
        #                     E=row['E'],
        #                     height=row['height/weight'][0:3],
        #                     weight=weight,
        #                     born_date=born_date,
        #                     position=row['position'],
        #                     career=row['career'],
        #                     starting_salary=starting_salary,
        #                     OPS=row['OPS']
        #                 )
        #
        # pprint.pprint(insert_dict)
        #
        # #     line_count = 0
        # #     for row in csv_reader:
        # #         if line_count == 0:
        # #             for i in range(len(row)):
        # #                 if row[i] not in insert_data:
        # #                     insert_data[row[i]]=[]
        # #     # print(insert_data.keys())
        # #         # if line_count != 0:
        # #         #     # for i in range(len(row)):
        # #         #     print(row[0])
        # #         #         # insert_data[row[i]].append(row[i])
        # #         if line_count != 0:
        # #             insert_data['batter_id'].append(row[0])
        # #             insert_data['batter_name'].append(row[1])
        # #             insert_data['year'].append(row[2])
        # #             insert_data['team'].append(row[3])
        # #             insert_data['avg'].append(row[4])
        # #             insert_data['G'].append(row[5])
        # #             insert_data['AB'].append(row[6])
        # #             insert_data['R'].append(row[7])
        # #             insert_data['H'].append(row[8])
        # #             insert_data['2B'].append(row[9])
        # #             insert_data['3B'].append(row[10])
        # #             insert_data['HR'].append(row[11])
        # #             insert_data['TB'].append(row[12])
        # #             insert_data['RBI'].append(row[13])
        # #             insert_data['SB'].append(row[14])
        # #             insert_data['CS'].append(row[15])
        # #             insert_data['BB'].append(row[16])
        # #             insert_data['HBP'].append(row[17])
        # #             insert_data['SO'].append(row[18])
        # #             insert_data['GDP'].append(row[19])
        # #             insert_data['SLG'].append(row[20])
        # #             insert_data['OBP'].append(row[21])
        # #             insert_data['E'].append(row[22])
        # #             insert_data['height_weight'].append(row[23])
        # #             insert_data['year_born'].append(row[24])
        # #             insert_data['position'].append(row[25])
        # #             insert_data['career'].append(row[26])
        # #             insert_data['starting_salary'].append(row[27])
        # #             insert_data['OPS'].append(row[28])
        # #
        # #
        # #         line_count += 1
        # #
        # # print(insert_data)
        #
        # # for row in insert_data:
        # #     print(row)
        create_table_name = "Pre_Season_Batter"
        sql_create = """
        CREATE TABLE IF NOT EXISTS `{}` (
        `batter_id` INT(11) NOT NULL,
        `batter_name` VARCHAR(50) COLLATE utf8_general_ci NOT NULL,
        `year`  YEAR(4) NOT NULL,
        `team` VARCHAR(50) COLLATE utf8_general_ci DEFAULT NULL,
        `avg` FLOAT DEFAULT NULL,
        `G` INT(11) DEFAULT NULL,
        `AB` INT(11) DEFAULT NULL,
        `R` INT(11) DEFAULT NULL,
        `H` INT(11) DEFAULT NULL,
        `H_2B` INT(11) DEFAULT NULL,
        `H_3B` INT(11) DEFAULT NULL,
        `HR` INT(11) DEFAULT NULL,
        `TB` INT(11) DEFAULT NULL,
        `RBI` INT(11) DEFAULT NULL,
        `SB` INT(11) DEFAULT NULL,
        `CS` INT(11) DEFAULT NULL,
        `BB` INT(11) DEFAULT NULL,
        `HBP` INT(11) DEFAULT NULL,
        `SO` INT(11) DEFAULT NULL,
        `GDP` FLOAT DEFAULT NULL,
        `SLG` FLOAT DEFAULT NULL,
        `OBP` FLOAT DEFAULT NULL,
        `height` INT(11) DEFAULT NULL,
        `weight` INT(11) DEFAULT NULL,
        `position` VARCHAR(50) COLLATE utf8_general_ci DEFAULT NULL,
        `career` VARCHAR(150) COLLATE utf8_general_ci DEFAULT NULL,
        `starting_salary` VARCHAR(20) COLLATE utf8_general_ci DEFAULT NULL,
        `OPS` FLOAT DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
        """.format(create_table_name)

        try:
            cur_db.execute(sql_create)
            cnx_db.commit()
        except:
            print(traceback.format_exc())

        sql_ins = """
        INSERT INTO {} (batter_id, batter_name, year, team, avg, G, AB, R, H, H_2B, H_3B, HR, TB, RBI,
        SB, CS, BB, HBP, SO, GDP, SLG, OBP, height, weight, position, career, starting_salary, OPS)
        VALUES
        (%(batter_id)s, %(batter_name)s, %(year)s, %(team)s, %(avg)s, %(G)s, %(AB)s, %(R)s, %(H)s,
        %(H_2B)s, %(H_3B)s, %(HR)s, %(TB)s, %(RBI)s, %(SB)s, %(CS)s, %(BB)s, %(HBP)s, %(SO)s, %(GDP)s,
        %(SLG)s, %(OBP)s, %(height)s, %(weight)s,%(position)s, %(career)s, %(starting_salary)s, %(OPS)s)
        """.format(create_table_name)

        idata = []
        for batter_id in insert_dict:
            for year in insert_dict[batter_id]:
                idata.append(dict(
                    batter_id=batter_id,
                    batter_name=insert_dict[batter_id][year]["batter_name"],
                    year=year,
                    team=insert_dict[batter_id][year]['team'],
                    avg=insert_dict[batter_id][year]['avg'],
                    G=insert_dict[batter_id][year]['G'],
                    AB=insert_dict[batter_id][year]['AB'],
                    R=insert_dict[batter_id][year]['R'],
                    H=insert_dict[batter_id][year]['H'],
                    H_2B=insert_dict[batter_id][year]['H_2B'],
                    H_3B=insert_dict[batter_id][year]['H_3B'],
                    HR=insert_dict[batter_id][year]['HR'],
                    TB=insert_dict[batter_id][year]['TB'],
                    RBI=insert_dict[batter_id][year]['RBI'],
                    SB=insert_dict[batter_id][year]['SB'],
                    CS=insert_dict[batter_id][year]['CS'],
                    BB=insert_dict[batter_id][year]['BB'],
                    HBP=insert_dict[batter_id][year]['HBP'],
                    SO=insert_dict[batter_id][year]['SO'],
                    GDP=insert_dict[batter_id][year]['GDP'],
                    SLG=insert_dict[batter_id][year]['SLG'],
                    OBP=insert_dict[batter_id][year]['OBP'],
                    height=insert_dict[batter_id][year]['height'],
                    weight=insert_dict[batter_id][year]['weight'],
                    position=insert_dict[batter_id][year]['position'],
                    career=insert_dict[batter_id][year]['career'],
                    starting_salary=insert_dict[batter_id][year]['starting_salary'],
                    OPS=insert_dict[batter_id][year]['OPS']
                ))
        try:
            cur_db.executemany(sql_ins, idata)
            cnx_db.commit()
        except:
            print(traceback.format_exc())

Worker().make_data()
