import os
import numpy as np
import pandas as pd
import requests
import time
# flask utils
from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

# define a flask app
application = Flask(__name__)
# application.secret_key = "secret_key"

# define global variable
UPLOAD_FOLDER = 'upload/'
# retrieve info through web API
URL = 'https://www.virustotal.com/vtapi/v2/file/report'
# replace it with your own api key
# you can get it by signing up on https://www.virustotal.com/gui/join-us
API_KEY = 'cdccfa9dc48fcfd4e39598112a100f8d268caab1cdfcc9a3e0fedc4dbd757151'


def query_api(hash_value):
	"""Query VirusTotal's API based on a given hash value"""
	try:
		params = {'apikey': API_KEY, 'resource': hash_value}
		response = requests.get(URL, params=params)
		results = response.json()
		fortinet_detect_name = results['scans']['Fortinet']['result']
		num_detect_eng = int(sum(
			[1 if results['scans'][x]['result'] else 0 for x in results['scans']]))
		scan_date = results['scan_date']
		return fortinet_detect_name, num_detect_eng, scan_date
	except:
		return 'None', 'None', 'None'


def retrieve_report(uploaded_file_path):
	"""Read uploaded file and return report as a dataframe"""
	df = pd.read_csv(uploaded_file_path, header=None,
					 names=['hash_value (MD5 or Sha256)'])
	ft_list, num_eng_list, scan_dt_list = [], [], []
	for i in range(len(df)):
		ft_nm, num_eng, scan_dt = query_api(
			df['hash_value (MD5 or Sha256)'][i])
		ft_list.append(ft_nm)
		num_eng_list.append(num_eng)
		scan_dt_list.append(scan_dt)
		time.sleep(15)
	df['Dectection name'] = ft_list
	df['Number of engines detected'] = num_eng_list
	df['Scan Date'] = scan_dt_list
	return df


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in 'txt'

# @: decorator
# map the url with the associated function
@application.route('/')
def index():
	return render_template('base.html')


# post: send the form data to the server
# get: default setting, send data in the unencrypted form to the server (form info may be shown in the url)
@application.route('/', methods=['POST'])
def upload_generate_report():
	"""Upload a txt file and display a query report"""
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('Please upload a file before generating the report')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if not os.path.exists(UPLOAD_FOLDER):
				os.makedirs(UPLOAD_FOLDER)
			file_path = os.path.join(UPLOAD_FOLDER, filename)
			file.save(file_path)
			print('File successfully uploaded')
			print('Start parsing file...')
			df = retrieve_report(file_path)
			print('Report generated')
			return render_template('results.html', name="Virus Scan Report",
								   tables=[df.to_html(classes='data table-hover ml-10', header="true")])
		else:
			flash('Allowed file type is txt')
			return redirect(request.url)


if __name__ == "__main__":
	# host: hostname to listen on. Set this to '0.0.0.0' to have the server available externally as well
	application.run(debug=True, host="0.0.0.0")