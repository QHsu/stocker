from flask import Flask, request, redirect, url_for
from flask import jsonify, make_response, render_template
from flask import Blueprint
from flask.views import MethodView
from sqlalchemy import asc, create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base
from database_setup import Basic_information, Month_revenue, Income_sheet
from database_setup import Balance_Sheet
import logging
from logging.handlers import TimedRotatingFileHandler
import json
import datetime

from stockerModel import (showMain, getStockNumber, handleBasicInfo,
                          handleIncomeSheet, handleMonthRevenue)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

logger = logging.getLogger()
BASIC_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
DATE_FORMAT = '%m-%d %H:%M'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)


app.add_url_rule('/',
                 'showMain',
                 view_func=showMain)
app.add_url_rule('/api/v0/stock_number',
                 'getStockNumber',
                 view_func=getStockNumber.as_view(
                     'getStockNumber_api'),
                 methods=['GET', 'POST'])
app.add_url_rule('/api/v0/basic_information/<string:stock_id>',
                 'handleBasicInfo',
                 view_func=handleBasicInfo.as_view(
                     'handleBasicInfo_api'),
                 methods=['GET', 'POST'])
app.add_url_rule('/api/v0/income_sheet/<string:stock_id>',
                 'handleIncomeSheet',
                 view_func=handleIncomeSheet.as_view(
                     'handlehandleIncomeSheet'),
                 methods=['GET', 'POST'])
app.add_url_rule('/api/v0/month_revenue/<string:stock_id>',
                 'handleMonthRevenue',
                 view_func=handleMonthRevenue.as_view(
                     'handleMonthRevenue'),
                 methods=['GET', 'POST'])


@app.errorhandler(404)
def pageNotfound(error):
    logging.info('Page not found: %s', (request.path))
    return make_response(json.dumps('404 not foundss'), 404)


@app.errorhandler(500)
def internalServerError(error):
    logging.error('Server Error: %s', (error))
    return make_response(json.dumps('404 not found'), 404)


if __name__ == '__main__':
    app.debug = True

    fileHandler = TimedRotatingFileHandler(
        'log/app.log', when='D', interval=1,
        backupCount=30, encoding='UTF-8', delay=False, utc=True)
    fileHandler.setFormatter(formatter)
    if app.debug is True:
        fileHandler.setLevel(logging.WARNING)
    else:
        fileHandler.setLevel(logging.WARNING)
    logger.addHandler(fileHandler)

    app.run(host='0.0.0.0', port=5000)
