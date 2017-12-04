# -*- coding: utf-8 -*-
# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
from google.cloud import bigquery
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


@app.route('/')
def index():
    
    baloons_list = """
        placemark_1 = new ymaps.Placemark([55.713181, 37.4818], {
                balloonContentHeader: \'ГБПОУ 1-Й МОК\',
                balloonContentBody: \'Место в <a href=\"https://www.mos.ru/dogm/function/ratings-vklada-school/ratings-2016-2017/\">рейтинге</a> 31\',
                balloonContentFooter: \'Доля  <a href=\"https://data.mos.ru/opendata/7719028495-rezultaty-ege-dogm\">ЕГЭ 220+</a>: 20%.<br>Доля  <a href=\"https://data.mos.ru/opendata/7719028495-rezultaty-ege-dogm\">ЕГЭ 160-</a>: 25%\',
                hintContent: \'Место в рейтинге 31\',
                iconContent: \'31\'
            });
        myMap.geoObjects.add(placemark_1);
    """.decode('utf8')
    
 #   client = bigquery.Client()    
 #   query_job = client.query("SELECT rating FROM plane_ratings.Moscow")
    
#    results = query_job.result(timeout=100)  # Waits for job to complete.
    
#    out = ""
#    for row in results:
#        out = out + "\n{}: ".format(row.rating)
    
#    return out
    
    return render_template('map.html',
                           all_baloons = "").replace("&#39;", "'")

# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
