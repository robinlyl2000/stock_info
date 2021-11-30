from flask import Flask,request
from resource.dailydata import getdailydata
from resource.dailydata import getdailyrate
from resource.company_info import get_company_info
from resource.rate_info import get_rate_info
from resource.stock_info import get_stock_info
import json
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/dailydata/<id>', methods=['GET'])
def dailydata(id):
    return getdailydata(id)

@app.route('/dailyrate', methods=['POST'])
def dailyrate():
    t = request.get_json()
    return getdailyrate(t)

@app.route('/company_info/<id>', methods=['GET'])
def company_info(id):
    return get_company_info(id)

@app.route('/rate_info/<id>', methods=['GET'])
def rate_info(id):
    return get_rate_info(id)

@app.route('/stock_info/<id>', methods=['GET'])
def stock_info(id):
    return get_stock_info(id)

if __name__ == '__main__':
    app.debug = True
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host = '0.0.0.0', port = 5000)