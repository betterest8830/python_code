#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import pandas as pd


def xlsx_to_csv(xlsx_f, csv_f, csv_code='utf8'):
    # 指定第一列为索引列，不然默认增加一列数字
    xlsx_data = pd.read_excel(xlsx_f, index_col=0)
    xlsx_data.to_csv(csv_f, encoding=csv_code)


def csv_to_txt(xlsx_f, csv_f, txt_f, csv_code='utf8', txt_code='txt'):
    xlsx_to_csv(xlsx_f, csv_f, csv_code)
    with codecs.open(txt_f, 'w', encoding=txt_code) as f:
        for line in codecs.open(csv_f, encoding=csv_code):
            line = line.strip()
            if not line:
                continue
            row_l = line.decode(encoding=csv_code).split(',')
            if u'ID' in row_l[0] or u'id' in row_l[0]:
                continue
            if len(row_l) != 3:
                print(row_l)
                if row_l[0] in [u'32896', u'209193']:
                    row_l = [row_l[0].strip(u'"'), row_l[1].strip(u'"'), row_l[2].strip(u'"') + u','.strip(u'"')]
                elif row_l[0] in [u'28346', u'210871']:
                    row_l = [row_l[0].strip(u'"'), row_l[1].strip(u'"')+u','+row_l[2].strip(u'"'), row_l[3].strip(u'"')]

                else:
                    continue

            #res_l = [tmp.replace(' ', '') for tmp in row_l]
            res_l = row_l
            #f.write(row_l[0] + u'\n')
            f.write(u'\t'.join(res_l[0:3]) + u'\n')


def csv_to_txt2(xlsx_f, csv_f, txt_f, csv_code='utf8', txt_code='GB18030'):
    xlsx_to_csv(xlsx_f, csv_f, csv_code)
    with codecs.open(txt_f, 'w', encoding=txt_code) as f:
        for line in codecs.open(csv_f, encoding=csv_code):
            line = line.strip()
            if not line:
                continue
            row_l = line.split(',')
            if len(row_l) != 5:
                print(row_l)
                continue
            f.write('\t'.join(row_l) + '\n')


if __name__ == '__main__':
    '''
    f_xlsx = 'new_cp/longyuedu.xlsx'
    f_csv = 'new_cp/longyuedu.csv'
    f_txt = 'new_cp/longyuedu.txt'
    csv_to_txt2(f_xlsx, f_csv, f_txt)
    '''
    cpname_list = [
        'huanwenshiji', 'lanyuezhongwen', 'longyuedu', 'luochenwenxue',
        'qichuangzhongwen', 'taoxiaoshuo', 'tianjindianyue', 'tianjinlixing'
    ]
    for cpname in cpname_list:
        print(cpname)
        f_xlsx = 'new_cp/%s.xlsx' % cpname
        f_csv = 'new_cp/%s.csv' % cpname
        f_txt = 'new_cp/%s.txt' % cpname
        csv_to_txt2(f_xlsx, f_csv, f_txt)
