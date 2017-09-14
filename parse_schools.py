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


i=0
res_file = open("res.txt", 'w')

for index, row in tidy.iterrows():
    i = i+1          
    var_name = 'placemark_{0}'.format(i)
    
    res = """
    var {0} = new YMaps.Placemark(new YMaps.GeoPoint({1},{2}));            
    {0}.name = "Место в рейтинге {4}";
    {0}.description = '{3}';
    map.addOverlay({0}); 
    """.format(var_name, row['X'].replace(',','.'), row['Y'].replace(',','.'), 
    row['school'].strip(), int(row['rating']))
           
    res_file.write(res)
    #print row['rating'], row['school']

res_file.close()