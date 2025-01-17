import random
import re
from typing import Dict, List
import uuid
from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from enum import Enum
import threading
import json
import requests
import urllib.parse


UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = set(['json'])
app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb://admin:admin@adapt-mongo-adapt.cp4ba-mission-16bf47a9dc965a843455de9f2aef2035-0000.eu-de.containers.appdomain.cloud:32535/LTI?authSource=admin'
app.config['CORS_Headers'] = 'Content-Type'
mongo = PyMongo(app)

@app.route('/api/swagger.json')
def swagger_json():
    # Read before use: http://flask.pocoo.org/docs/0.12/api/#flask.send_file
    return send_file('swagger.json')


SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={  # Swagger UI config overrides
    'app_name': "Add/update JD"
},)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.get('/common-assets')
def commonassets():
    url = request.args.get("url")
    url = "https://cpd-ibm-cloudpaks.icp4auto-partnership-2bd2c162965d593cc66365794b1d3a7f-0000.jp-tok.containers.appdomain.cloud/bas/dba/studio/platform/common-assets/"
    payload={}
    headers = {
    'BPMCSRFToken':'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzgzNjU5MjAsInN1YiI6ImNlYWRtaW4ifQ.UFNxL6nxUsK_UtCVuZ5kaMc3AokEqlynli_yA-EOgAs',
    'Accept': 'application/json',
    'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz',
    }
    print(headers)
    response = requests.request("GET", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/detail')
def detail():
    id = request.args.get("id")
    url = "https://cpd-ibm-cloudpaks.icp4auto-partnership-2bd2c162965d593cc66365794b1d3a7f-0000.jp-tok.containers.appdomain.cloud/bas/dba/studio/platform/common-assets/<id>/versions?optional_parts=operations%2Corigin"
    getURL = url.replace("<id>", id)
    print(getURL)
    payload={}
    headers = {
    'BPMCSRFToken': 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzgzNjU5MjAsInN1YiI6ImNlYWRtaW4ifQ.UFNxL6nxUsK_UtCVuZ5kaMc3AokEqlynli_yA-EOgAs',
    'Accept': 'application/json',
    'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz',
    'Cookie': 'BAS-JSESSIONID=0000MORj4MM7LbZcbChXbaewO6l:89871766-68ff-4602-8fce-69846f5d05d0; __preloginurl__=/bas/dba/studio/platform/common-assets/; basLtpaToken2=DWX3lyWMw0HHJDk9y5WXiDbSd3khUKB4Z2Bjtc+l6MWJRYrBSUxU/6JcklN+c5UyAXTUPZprf2G68N+Hh2GyimNEjOt9huWyGgLQG6xKZPiMV/EgAsHOENqK8vLjtaesOaI+TFrmGx+dUzwQ6jr9BYLZtOxOtXxx8KQbe8nfJILFy7qv5kUCfHzjr4fLNAqumGoz2FqeSGqOyN+qKMgAzUNaBdsZpIHMfjhOgOPeTJ+13Y5M1sP2irmQZzFS7IdVmhwKcYdJlXhq7+NAYUUmNyOxqJvPkAR3Uisyr1ZtXq12Bg4OC81t2oSzqcJNjcM4Kzs/8pQqZDKFkmh6INNcjuMNFIfxbLU3vBKVbHHSpUa3OD97KjEXD0mgu3zg2TgRgX/O4lYnkH7+9Nfd6uEQfNX2gxSxxrP80+k+SQifOXW++MWyf0t7Pc9su0VtAYAL'
    }
    response = requests.request("GET", getURL, headers=headers, data=payload,verify=False)
    return (response.text)

@app.route('/auth', methods=['POST'])
def auth():
    input = request.get_json()
    url = "https://account.uipath.com/oauth/token"
    payload = json.dumps({
    "grant_type": "refresh_token",
    "client_id": input["client_id"],
    "refresh_token": input["refresh_token"],
    })
    headers = {
    'Content-Type': 'application/json'    }
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/folders')
def folders():
    url = "https://cloud.uipath.com/ibmiruyvjn/TestAutomation/orchestrator_/odata/folders"

    headers = {
    'Authorization': 'Bearer '+request.headers.get('Authorization')
    }
    payload={}

    response = requests.request("GET", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/Releases')
def Releases():
    url = "https://cloud.uipath.com/ibmiruyvjn/TestAutomation/odata/Releases"
    release_id = request.args.get("release")
    payload={}
    headers = {
    'X-UIPATH-OrganizationUnitId': release_id,
    'Authorization': 'Bearer '+request.headers.get('Authorization')
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return (response.text)

@app.post('/StartProcess')
def StartProcess():
    input = request.get_json()

    url = "https://cloud.uipath.com/ibmiruyvjn/TestAutomation/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"

    payload = json.dumps({
    "startInfo": {
        "ReleaseKey": input["key"],
        "Strategy": "ModernJobsCount",
        "JobsCount": 1,
        "InputArguments": "{}"
    }
    })
    print(payload)
    headers = {
    'Content-Type': 'application/json',
    'X-UIPATH-OrganizationUnitId': input['folder_id'],
    'Authorization': 'Bearer '+request.headers.get('Authorization')
    }
    print(headers)
    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    return (response.text)

@app.get('/openapi')
def openapi():
    name = request.args.get("name")
    project_name = request.args.get("project_name")

    url = "https://cpd-ibm-cloudpaks.icp4auto-partnership-2bd2c162965d593cc66365794b1d3a7f-0000.jp-tok.containers.appdomain.cloud/bawaut/automationservices/rest/<project_name>/<name>/docs"
    reeplace_projectName = url.replace("<project_name>",project_name)
    replace_name = reeplace_projectName.replace("<name>",name)

    payload={}
    headers = {
        'BPMCSRFToken': 'eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NzgzNjU5MjAsInN1YiI6ImNlYWRtaW4ifQ.UFNxL6nxUsK_UtCVuZ5kaMc3AokEqlynli_yA-EOgAs',
        'Accept': 'application/json',
        'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz',
        'Cookie': 'BAS-JSESSIONID=0000MORj4MM7LbZcbChXbaewO6l:89871766-68ff-4602-8fce-69846f5d05d0; __preloginurl__=/bas/dba/studio/platform/common-assets/; basLtpaToken2=DWX3lyWMw0HHJDk9y5WXiDbSd3khUKB4Z2Bjtc+l6MWJRYrBSUxU/6JcklN+c5UyAXTUPZprf2G68N+Hh2GyimNEjOt9huWyGgLQG6xKZPiMV/EgAsHOENqK8vLjtaesOaI+TFrmGx+dUzwQ6jr9BYLZtOxOtXxx8KQbe8nfJILFy7qv5kUCfHzjr4fLNAqumGoz2FqeSGqOyN+qKMgAzUNaBdsZpIHMfjhOgOPeTJ+13Y5M1sP2irmQZzFS7IdVmhwKcYdJlXhq7+NAYUUmNyOxqJvPkAR3Uisyr1ZtXq12Bg4OC81t2oSzqcJNjcM4Kzs/8pQqZDKFkmh6INNcjuMNFIfxbLU3vBKVbHHSpUa3OD97KjEXD0mgu3zg2TgRgX/O4lYnkH7+9Nfd6uEQfNX2gxSxxrP80+k+SQifOXW++MWyf0t7Pc9su0VtAYAL'
        }
    print(replace_name)
    response = requests.request("GET", replace_name, headers=headers, data=payload,verify=False)
    return (response.text)
    
@app.get('/ui-spec')
def uiSpec():
    f = open('ui-path.json')
    data = json.load(f)
    return (data)

@app.get('/openapi_ADS')
def openapi_ADS():
    decision_id = request.args.get("id")
    url = "https://cpd-ibm-cloudpaks.icp4auto-partnership-2bd2c162965d593cc66365794b1d3a7f-0000.jp-tok.containers.appdomain.cloud/ads/runtime/api/v1/deploymentSpaces/embedded/decisions/<decision_id>/openapi?outputFormat=JSON"
    encoded_decision_id=urllib.parse.quote(decision_id, safe='')
    print("decisionid encoded",encoded_decision_id)
    replace_decision_id_url= url.replace("<decision_id>",encoded_decision_id)
    payload={}
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkplYXBsQUdrUEhqbXQ3c2ZibHNmRkNmN09uSjE1blY2UFEwM3dYcFZFRUkifQ.eyJ1c2VybmFtZSI6ImNlYWRtaW4iLCJzdWIiOiJjZWFkbWluIiwiaXNzIjoiS05PWFNTTyIsImF1ZCI6IkRTWCIsInJvbGUiOiJBZG1pbiIsInBlcm1pc3Npb25zIjpbImFkbWluaXN0cmF0b3IiLCJjYW5fcHJvdmlzaW9uIiwibWFuYWdlLWRhdGEtYWNjZXNzIiwibWFuYWdlLXRlbXBsYXRlLWRhc2hib2FyZHMiLCJjYW5fYWRtaW5pc3RyYXRlX2J1c2luZXNzX3RlYW1zIiwiY2FuX3dvcmtfd2l0aF9iYV9hdXRvbWF0aW9ucyJdLCJncm91cHMiOlsxMDAwMF0sInVpZCI6IjEwMDAzMzEwMDIiLCJhdXRoZW50aWNhdG9yIjoiZXh0ZXJuYWwiLCJkaXNwbGF5X25hbWUiOiJjZWFkbWluIiwiY2FuX3JlZnJlc2hfdW50aWwiOjE2NzgzNzk0NzE4MDcsImNzcmZfdG9rZW4iOiI0Nzg3MjBlNjJiZDZiNmYxZjBmMTBkZDBjNWQ4ZjY1NiIsInNlc3Npb25faWQiOiI0ZWU1YmU2MC0xNmUzLTRhOTYtOTQ2MC02ODk4MGZhMTVhY2IiLCJpYW0iOnsiYWNjZXNzVG9rZW4iOiJkZGU5MzBjYWE0MDRhZjJlMjZhNDcyMGVkMjdhM2IwOTMxNDE1YmZjMDc1NWUyODI3Mzk2MDc2ZDdkZDgwYmMyNTdmOWYzZGVhMWI2OGM0ODE5ZmI5NWMxMDQ0MmE1ODg0ZDZkNDQzYTMyNWY5ZWQxNGEzMjRlM2Y2ZDlmMDcwYjM3Y2RkM2ZmZmI4NTMwYWY2NTRjNTQ1Yjk2ZmM4N2E0NThjZmU3ODI1YWI5NzRmYWY4MmRhNzk5MGZmODJjYjJhYzFkNzVmNzdmNDc2NWI3NGRhM2U4NjRmNzdmYzFkZDVmYmZlNmVjNDNiNzZjZTMzMzk4MGQ2NzIwZjhmZmFhZTVlODM4NjBkODg1NmZlMTI1MTU5ZjdmM2RhOThlMzMxMTcyZGE5MzU1OGI2NzA2ODdjNDdjMDNhMjg1NjE5MmRkZTlmMDNhMWI5ZjljZTUzZWZlNWJiMTgyZjFhZTJjMTk0MjlmM2Y3ZmY0NzYxZWQ2YzdjOTM3NWE4MWRkYmFmYjIxZGViZGE3MWVlMzBlM2VjNTU0YjdhMDEyNTRmMGU3ZThmNTZmMGUyZmI4MDJkNDUzN2MxYTdlOWIxNWZmNGQyMTQ5NmQ1YjUyNTg0ZjRhOTNkOWE0YjBhNDIxMDQ4MGFiOTAxMjlhZmM1MGY4NmFhNTllZmU3ZjRiYzMzOTk1ZTNjMDcwMjM5ZDJkZTIzZDdkOGI1NGQ1NGRjMzczZDg5NTAzMTc4MmU3YjNlYTRiMWM3NjI3ZDM2MWQxMmFhM2NkNzU3NWQzMDEwMzVkNmU0NTA2Y2I4NWRkMTU0MzNmOTU4NTdhZTQ0ZDliNzdkMmY5N2Y0M2IzODczY2E3ZWFiNDhmMmRmZTA5MzhiNTZmNDMzZWY1ZmNjNjUzZDhhZTg5NjY2ZGVkY2UxNDExZjhlNTVlYWE3NDM4NGVjN2IwYTgzYjk0ZDQ1YTkzNDI3OWM3MTAyNTNhMzg2ZTJmNmE4NmE0OTIwNWU2YTJhZDMyZjQwZGQxMGI0M2IwMDg0Y2Q0M2VlZTFiMmJiZTY0YzZjYThiYzAzMWYxZDM3ZDUwYWViMTQyNjcyZjY1MzBlNTc2YjUwMGQ3NGE5OGY0NGI1YzUxNzZhYzI5MzdhZDMyYmZlYWNiZGUwZGI4YzI5NDc5ZWE3ZTRiY2I3ZTA5NzczNzUwODNjYTMzYWFlY2Q1NjViZGE1NGI5M2YxZWI0Y2QyZmNiZjc0OTg5NGFlZTYwMGZkMjcwY2Y0MTlhY2EzMmNlYjhkNDVlNjRjZjVjMGY3YjNlMzM1MmFjNDM2ZWMwNjg4OTk4ZWM4YjQ2NzY5OTFjZGEwMmE3ZjhjNmRlMWM4YzU3MWVjZGQwNzEyIn0sImlhdCI6MTY3ODMzNjMwNywiZXhwIjoxNjc4Mzc5NTA3fQ.EPRrMTxvAq2AJSTFMijO-QbAgdvqHH-5ZT-tHvG967lvOPPA32pEWszj70Y9g-aL_WYah0gsGJS8SODXPLGaDhUtS4kuuBQxeD7YG4goyvwNFeo8elCmto_WbHy85QNijSoha9PWyUEHYKX29IOXFG-yhdLHle8gjRIv3zsuCSFwm6aNFuFnSJ45HMYB2FXD4t2_gqphVSH8qhshehEQwp-VFF6LT2jrOskDjapKZkwuMCMnT192YkpC4dE0mLCC6EnXg84RUgIBDD_uVCBU2MCbpXS8a6nPBRtTDjPvlDc8U9a2juMkSLlz4lnhP_OCcIUKgAv5mBxL75XVT8XjJA',
        }
    print("url",replace_decision_id_url)

    response = requests.request("GET", replace_decision_id_url, headers=headers, data=payload,verify=False)
    print(response)
    return (response.text)

@app.post('/getToken')
def getCSRFToken():
    url = request.args.get("url")
    url = url+"/bawaut/ops/system/login"
    payload=json.dumps({
    "refresh_groups": True,
    "requested_lifetime": 10800000
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Basic Y2VhZG1pbjpjZWFkbWluMTIz',
        }

    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    json_response=json.loads(response.content.decode('utf-8'))
    print(json_response)
    csrftoken = {"data":json_response["csrf_token"]}
    return csrftoken

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
