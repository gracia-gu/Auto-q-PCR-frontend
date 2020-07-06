from application import app
from flask import render_template, request, make_response, redirect, flash
import io
import pandas as pd
from application import AUTOqPCR, plot, statistics
import datetime
from zipfile import ZipFile


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	return render_template('index.html', index=True)


@app.route('/form')
def form():
	return render_template('form.html', form=True)


@app.route('/download', methods=["POST"])
def transform_view():
	files = request.files.getlist('file[]')
	if len(files) == 0:
		return "No file"
	# Creates empty data frame
	data = pd.DataFrame()

	for item in files:
		stream = io.StringIO(item.stream.read().decode("utf-8"), newline="")
		i = 0
		while True:
			h = stream.readline()
			if not h:
				i = -1
				break
			# if not h.replace(",",""):
			# i += 1
			if h.upper().startswith("WELL"):
				break
			i += 1
		if i == -1:
			print("No header found in '{}'".format(item))
			continue
		else:
			print("Header found at {} in '{}'".format(i, item))
		# print(i)

		stream.seek(0)
		filedata = pd.read_csv(stream,
							   skip_blank_lines=True,
							   skipinitialspace=True,
							   engine='python',
							   encoding="utf-8",
							   header=i)

		# print(filedata)
		filedata.rename(columns=rx_rename, inplace=True)
		data = data.append(filedata, ignore_index=True, sort=True)
		data['filename'] = item.filename

	# stream.seek(0)

	model = request.form['option']
	cgenes = request.form['cgenes']
	cutoff = request.form.get('cutoff', type=float)
	max_outliers = request.form.get('max_outliers', type=float)
	target_sorter = request.form['target_sorter']
	sample_sorter = request.form['sample_sorter']
	csample = request.form['csample']
	colnames = request.form['colnames']
	qty = request.form.get('quantity', type=int)
	gcol = request.form['gcol']
	glist = request.form['glist']
	rm = request.form['option2']
	nd = request.form['option4']

	# making log.txt file
	log = 'Model: ' + model + '\nEndogenous control genes: ' + cgenes + '\nCut-off: ' + str(cutoff) + \
		  '\nMaximum Outliers: ' + str(max_outliers) + '\nTarget Order: ' + target_sorter + '\nSample Order: ' + \
		  sample_sorter + '\nControl Sample: ' + csample + '\nAdditional column names: ' + colnames + \
		  '\nNumber of groups: ' + str(qty) + '\nGroup column name: ' + gcol + '\nGroup name: ' + glist + \
		  '\nRepeated measures: ' + rm + '\n' + 'Normal distribution: ' + nd + '\n'

	clean_data, summary_data, targets, samples = AUTOqPCR.process_data(data, model, cgenes, cutoff, max_outliers,
																  target_sorter, sample_sorter, csample, colnames)

	plots = plot.plots(summary_data, model, targets, samples)
	plots2 = plot.plots_wo_controls(summary_data, model, targets, samples, cgenes)

	# making stats csv
	if qty is not None:
		if request.form['option3'] != 'False':
			if gcol.lower() in clean_data.columns.str.lower():
				col = gcol
			clean_data['Group'] = clean_data[col]
		else:
			groups = glist.split(',')
			clean_data = statistics.add_groups(clean_data, groups)

		group_plot = plot.plot_by_groups(clean_data, model, targets, cgenes)

		stats_dfs, posthoc_dfs = statistics.stats(model, qty, clean_data, targets, rm, nd)
		stats_output = stats_dfs.to_csv(index=False)
		posthoc_output = posthoc_dfs.to_csv(index=False)

	# making summary data csv
	output = summary_data.to_csv()
	clean_output = clean_data.to_csv()

	outfile = io.BytesIO()
	with ZipFile(outfile, 'w') as myzip:
		if qty is not None:
			if qty == 2:
				if nd == 'True':
					myzip.writestr('ttest_result.csv', stats_output)
				else:
					if rm == 'True':
						myzip.writestr('MannWhitneyUTest_result.csv', stats_output)
					else:
						myzip.writestr('WilcoxonTest_result.csv', stats_output)
			else:
				if nd == 'True':
					myzip.writestr('ANOVA_result.csv', stats_output)
					myzip.writestr('Posthoc_result.csv', posthoc_output)
				else:
					if rm == 'True':
						myzip.writestr('Friedman_result.csv', stats_output)
					else:
						myzip.writestr('KruskalWallisTest_result.csv', stats_output)
					myzip.writestr('Posthoc_result.csv', posthoc_output)

			buf = io.BytesIO()
			group_plot[0].savefig(buf)
			image_name = 'Plot_by_groups.png'
			myzip.writestr(image_name, buf.getvalue())
			buf.close()
			buf = io.BytesIO()
			group_plot[1].savefig(buf)
			image_name2 = 'Plot_by_targets.png'
			myzip.writestr(image_name2, buf.getvalue())
			buf.close()
		myzip.writestr('clean_data.csv', clean_output)
		myzip.writestr('summary_data.csv', output)
		myzip.writestr('log.txt', log)
		# individual plots
		for i in range(len(plots) - 2):
			buf = io.BytesIO()
			plots[i].savefig(buf)
			if model != 'instability':
				image_name = targets[i] + '.png'
				myzip.writestr(image_name, buf.getvalue())
		# grouped plots by sample and by genes
		buf = io.BytesIO()
		plots[len(plots) - 2].savefig(buf)
		image_name = 'Sample_Groups.png'
		myzip.writestr(image_name, buf.getvalue())
		buf.close()
		buf = io.BytesIO()
		plots[len(plots) - 1].savefig(buf)
		image_name = 'All_Targets.png'
		myzip.writestr(image_name, buf.getvalue())
		buf.close()
		if model != 'instability':
			# plots with endogeneous controls removed
			buf = io.BytesIO()
			plots2[0].savefig(buf)
			image_name = 'Sample_Groups (without endogenous controls).png'
			myzip.writestr(image_name, buf.getvalue())
			buf.close()
			buf = io.BytesIO()
			plots2[1].savefig(buf)
			image_name = 'All_Targets (without endogenous controls).png'
			myzip.writestr(image_name, buf.getvalue())
			buf.close()
			myzip.close()

	# get current machine time
	now = datetime.datetime.now()
	date_string = now.strftime("%m-%d-%Y")

	response = make_response(outfile.getvalue())
	response.headers['Content-Type'] = 'application/actet-stream'
	response.headers['Content-Disposition'] = 'attachment; filename=outputs_' + model + '_' + date_string + '.zip'
	outfile.close()

	# get CPU and memory for the process
	# myProcess = psutil.Process(os.getpid())
	# print('CPU percent: ' + str(myProcess.cpu_percent()))
	# print('Memory info: ' + str(myProcess.memory_info()[0]/2.**30))

	return response


@app.route('/help')
def user_guide():
	return render_template('help.html', user_guide=True)


@app.route('/contact')
def contact():
	return render_template('contact.html', contact=True)
