# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:57:49 2017

@author: minushkin
"""

import pandas as pd
import re

raw_rating = pd.read_csv('./data/rating_unicode.txt', 
                         names = ["rating", "school"])


#s = raw_rating.iloc(1)[1].school
def get_school_number(s):
    x = re.findall("\\d+", s)
    if len(x) ==1:
        return int(x[0])
    
    return 0
    
raw_rating['number'] = raw_rating['school'].apply(get_school_number)

rating = raw_rating.set_index('number')

#rating = rating[rating.rating < 50]

def extract_numbers_and_coords(path, sep):
    raw_schools = pd.read_csv(path, sep=sep)
    raw_schools['number'] = raw_schools['name'].apply(get_school_number)
    return raw_schools[['number','X','Y']].set_index('number')
    
# schools
schools = extract_numbers_and_coords('./data/data-20130909T0800.csv', sep=';')

# liceums
liceums = extract_numbers_and_coords(
        './data/data-20131031T1206-structure-20131031T1206.csv', 
        sep=',')


gimnasiums = extract_numbers_and_coords(
        './data/data-20131031T1325-structure-20131031T1325.csv', 
        sep=',')

all_schools = pd.concat([schools, liceums, gimnasiums], axis = 0)

tidy = pd.merge(left = rating.iloc[rating.index != 0],
                right = all_schools.iloc[all_schools.index != 0][['X', 'Y']],
                how='inner', 
                left_index=True,
                right_index=True)


# ЕГЭ 205-2016

ege_rating = pd.read_csv('./data/data-9722-2016-10-31.csv', sep=';')
ege_rating['number'] = ege_rating['EDU_NAME'].apply(get_school_number)
ege_rating = ege_rating.set_index('number')

tidy2 = pd.merge(left = tidy,
                right = ege_rating.iloc[ege_rating.index != 0][['PASSED_NUMBER_FULL', 'PASSES_OVER_220', 'PASSER_UNDER_160']],
                how='inner', 
                left_index=True,
                right_index=True)

import matplotlib.pyplot as plt

plt.scatter(tidy2['rating'], tidy2['PASSES_OVER_220']/tidy2['PASSED_NUMBER_FULL'] * 100)

plt.scatter((tidy2['PASSED_NUMBER_FULL'] - tidy2['PASSER_UNDER_160'])/tidy2['PASSED_NUMBER_FULL'] * 100, 
            tidy2['PASSES_OVER_220']/tidy2['PASSED_NUMBER_FULL'] * 100)


plt.scatter((tidy2['PASSER_UNDER_160'] - tidy2['PASSES_OVER_220'])/tidy2['PASSED_NUMBER_FULL'] * 100, 
            tidy2['PASSES_OVER_220']/tidy2['PASSED_NUMBER_FULL'] * 100)



i=0
res_file = open("res_3.txt", 'w')

for index, row in tidy2.iterrows():
    i = i+1          
    var_name = 'placemark_{0}'.format(i)
    
    res = """
    {0} = new ymaps.Placemark([{2}, {1}], {{
                balloonContentHeader: '{3}',
                balloonContentBody: 'Место в <a href=\\"https://www.mos.ru/dogm/function/ratings-vklada-school/ratings-2016-2017/\\">рейтинге</a> {4}',
                balloonContentFooter: 'Доля  <a href=\\"https://data.mos.ru/opendata/7719028495-rezultaty-ege-dogm\\">ЕГЭ 220+</a>: {5}%.<br>Доля  <a href=\\"https://data.mos.ru/opendata/7719028495-rezultaty-ege-dogm\\">ЕГЭ 160-</a>: {6}%',
                hintContent: 'Место в рейтинге {4}',
                iconContent: '{4}'
            }});
        myMap.geoObjects.add({0});""".format(var_name, 
        row['X'].replace(',','.'), 
        row['Y'].replace(',','.'), 
        row['school'].strip().replace('"', ''), 
        int(row['rating']),
        int(float(row['PASSES_OVER_220'])/row['PASSED_NUMBER_FULL'] * 100),
        int(float(row['PASSED_NUMBER_FULL'] - row['PASSER_UNDER_160'])/row['PASSED_NUMBER_FULL'] * 100)
        )
           
    res_file.write(res)
    #print row['rating'], row['school']

res_file.close()

#####




