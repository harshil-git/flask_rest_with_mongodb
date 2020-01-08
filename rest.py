from flask import Flask, jsonify, request
import pymongo
from pymongo import MongoClient
import json
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/rest_api.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(lineno)d]'))
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('rest_api in use')

connection = MongoClient('localhost',27017)

db = connection['Rest_db']
col = db['Frameworks']

@app.route('/frameworks', methods=['GET'])
def get_all_frameworks():
    try:
        if col:
            
            output = []

            for q in col.find():
                output.append({'name' : q['name'], 'description' : q['description']})

            return jsonify({'result' : output})
    except Exception as error:
        return app.logger.error(error)
        #jsonify({'Error':str(error)})

@app.route('/frameworks/<name>', methods=['GET'])
def get_one_framework(name):
    try:
        if col:

            q = col.find_one({'name' : name})

            if q:
                output = {'name' : q['name'], 'description' : q['description']}
            return jsonify({'result' : output})
    except Exception as error:
        return app.logger.error(error)
   

    

@app.route('/frameworks', methods=['POST'])
def add_framework():
    try:
        if col:

            name = request.json['name']
            description = request.json['description']

            framework_id = col.insert({'name' : name, 'description' : description})
            new_framework = col.find_one({'_id' : framework_id})

            output = {'name' : new_framework['name'], 'description' : new_framework['description']}

            return jsonify({'result' : output})
    except Exception as error:
        return app.logger.error(error)


@app.route('/frameworks/<name>', methods=['PUT'])
def update_framework(name):
    try:
        name = request.json['name']
        description = request.json['description']
        q = col.find({"_id":name})
        if q:
            val=col.update_one({'name': name}, {'$set': {'description': description}})
        else:
            app.logger.error("Data not Found")
    except Exception as error:
        return app.logger.error(error)
    return "Successfully data updated"


@app.route('/frameworks/<name>', methods=['DELETE'])
def delete_one_framework(name): 
    try:
        
        if col:
        
            if col.find_one({'name': name}) == None:
                raise Exception
            else:
                col.delete_one({'name': name})
                output = "{} deleted successfully!".format(name)

            return jsonify({'result': output})
    except Exception as error:
        return app.logger.error(error)


if __name__ == '__main__':
    app.run(debug=True)