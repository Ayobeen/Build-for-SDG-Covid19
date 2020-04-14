from flask import Flask, request, render_template, make_response, g, jsonify
import json
import time




# Init app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'faddc0c0f6e8d2b5e7507087d1114da6'

# Reading Json Input
output = ""
@app.route('/api/v1/on-covid-19', methods=['POST']) #GET requests will be blocked
def estimators(data):
	input_data = request.get_json()

	data = input_data['data']['region']
	periodType = input_data['data']['periodType']
	timeToElapse = input_data['data']['timeToElapse']
	reportedCases = input_data['data']['reportedCases']
	population = input_data['data']['population']
	totalHospitalBeds = input_data['data']['totalHospitalBeds']

# Cleaning Input Data
	periodType = periodType.lower()
	if periodType == 'days':
		timeToElapse = timeToElapse
	elif periodType == 'weeks':
		timeToElapse = timeToElapse*7
	else:
		timeToElapse = timeToElapse*30
	factor = timeToElapse // 3

# Computing Input Data for Impact	
	currentlyInfected = reportedCases * 10
	infectionsByRequestedTime = currentlyInfected * 2**factor
	#Challenge 2
	severeCasesByRequestedTime = int(15 * 0.01 * infectionsByRequestedTime)
	currentlyAvailableBeds = totalHospitalBeds * 0.35
	hospitalBedsByRequestedTime = int(currentlyAvailableBeds - severeCasesByRequestedTime)

	#Challenge 3
	casesForICUByRequestedTime = int( 0.05 * infectionsByRequestedTime)
	casesForVentilatorsByRequestedTime = int(0.02 * infectionsByRequestedTime)
	dollarsInFlight = int((infectionsByRequestedTime 
						* data['avgDailyIncomePopulation'] 
						* data['avgDailyIncomeInUSD']
						/ timeToElapse))

	# Computing Input Data for SevereImpact
	SIcurrentlyInfected = reportedCases * 50
	SIinfectionsByRequestedTime = SIcurrentlyInfected * 2**factor
	#Challenge 2
	SIsevereCasesByRequestedTime = int(15 * 0.01 * SIinfectionsByRequestedTime)
	SIcurrentlyAvailableBeds = totalHospitalBeds * 0.35
	SIhospitalBedsByRequestedTime = int(SIcurrentlyAvailableBeds - SIsevereCasesByRequestedTime)

	#Challenge 3
	SIcasesForICUByRequestedTime = int( 0.05 * SIinfectionsByRequestedTime)
	SIcasesForVentilatorsByRequestedTime = int(0.02 * SIinfectionsByRequestedTime)
	SIdollarsInFlight = int((SIinfectionsByRequestedTime 
						* data['avgDailyIncomePopulation'] 
						* data['avgDailyIncomeInUSD']
						/ timeToElapse))
	# Outputing Result
	global output
	output = {
			"data":{
		  "region":{
			"name":data["name"],
			"avgAge": data['avgAge'],
			"avgDailyIncomeInUSD": data['avgDailyIncomeInUSD'],
			"avgDailyIncomePopulation": data['avgDailyIncomePopulation']
		},
		"periodType":periodType,
		"timeToElapse":timeToElapse,
		"reportedCases":reportedCases,
		"population":population,
		"totalHospitalBeds":totalHospitalBeds
		},

		"estimate" : {
			"impact" : {
				"currentlyInfected" : currentlyInfected,
				"infectionsByRequestedTime" : infectionsByRequestedTime,
				"severeCasesByRequestedTime" : severeCasesByRequestedTime,
				"hospitalBedsByRequestedTime" : hospitalBedsByRequestedTime,
				"casesForICUByRequestedTime" : casesForICUByRequestedTime,
				"casesForVentilatorsByRequestedTime" : casesForVentilatorsByRequestedTime,
				"dollarsInFlight" : dollarsInFlight
				},
			"severeImpact" : {
				"currentlyInfected" : SIcurrentlyInfected,
				"infectionsByRequestedTime" : SIinfectionsByRequestedTime,
				"severeCasesByRequestedTime" : SIsevereCasesByRequestedTime,
				"hospitalBedsByRequestedTime" : SIhospitalBedsByRequestedTime,
				"casesForICUByRequestedTime" :SIcasesForICUByRequestedTime,
				"casesForVentilatorsByRequestedTime" : SIcasesForVentilatorsByRequestedTime,
				"dollarsInFlight" : SIdollarsInFlight
			}

		}

	}
	

	estimate_schema = json.dumps(output, sort_keys =False, indent =4)
	data = estimate_schema
	return data
	

"""
# Request/Response Time Different Logging

@app.before_request
def start_timer():
    g.start = time.time()

duration = " "
responseCode = " "
@app.after_request
def log_request(response):

	now = time.time()
	global duration
	duration = round(now - g.start, 6)
	global responseCode
	responseCode = response.status_code
	method = request.method
	path = request.path
	logData = {}
	logData['logs'] = []
	logData['logs'].append({
		'method': method,
		'path': path,
		'duration': duration,
		'responseCode': responseCode
		})

	with open('logData.txt', 'a') as outfile:
		for logs in logData:
			json.dump(logData, outfile, indent=2)
			#outfile.write('\n')
			return response

# Frontend Challenge

@app.route("/test")
def welcome():
	return render_template('welcome.html', title ='welcome')


@app.route("/api/v1/on-covid-19/xml", methods=['POST'])
def xml():
	my_xml_resp = make_response('Response!')
	my_xml_resp.mimetype = 'application/xml'




	from dicttoxml import dicttoxml
	
	xml = dicttoxml(output, attr_type=False)
	print (xml)
	return xml

import xml.etree.cElementTree as e
	r = e.Element("CovidData")
	data = e.SubElement(r,"data")
	for z in estimate_schema["data"]:
		e.SubElement(data,"Topic").text = z["Topic"]


@app.route('/api/v1/on-covid-19/logs')
def query_example():
	my_json_resp = make_response('Response!!')
	my_json_resp.mimetype = 'application/xml'

	with open('logData.txt') as json_file:
		data = json_file.read()
		new_data = data.replace('}{', '},{')
		logs_list = json.loads(f'[{new_data}]')
		print(logs_list)
		for logs in logs_list:
			for data in logs:
				for items in data:

					print(data[items])


					return items['method'], items['path'], items['duration'], items['responseCode']






@app.before_request
def before_request():
    g.start = time.time()
    #g.request_time = lambda: "%.5fs" % (time.time() - g.start)
    

@app.after_request
def log_request(response):
	if request.path == '/favicon.ico':
		return response
	elif request.path.startswith('/static'):
		return response

@app.route("/logs")
def logs():
    
    return g.start()

data = [
{
  "logs": [
    {
      "method": "GET",
      "path": "/api/v1/on-covid-19/xml",
      "duration": 0.001,
      "responseCode": 404
    }
  ]
},
{
  "logs": [
    {
      "method": "GET",
      "path": "/api/v1/on-covid-19/",
      "duration": 0.001,
      "responseCode": 404
    }
  ]
}
]
"""

# Run Server
if __name__ == '__main__':
	app.run(debug=True)
