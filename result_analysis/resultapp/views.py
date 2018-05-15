from django.contrib.auth import views
from django.shortcuts import render, get_object_or_404, redirect
from .models import Result
from django.http import JsonResponse
import json
from django.core import serializers
from collections import OrderedDict

def getResultSession():
	result_dict = {}

	# Dropdown for years
	years = Result.objects.values_list("AcademicYear").distinct()
	for year in years:
		temp = year[0].split("-")
		result_dict["Winter " + str(temp[0])] = []
		result_dict["Summer " + str(temp[1])] = []
	print("Successfully fetch years!")

	# Dropdown values for result year
	exams = Result.objects.values_list("AcademicYear", "exam").distinct()
	for exam in exams:
		exam_year, exam_name = exam
		temp = exam_year.split("-")
		if temp[0] in exam_name:
			result_dict["Winter " + str(temp[0])].append(exam_name)
		elif temp[1] in exam_name:
			result_dict["Summer " + str(temp[1])].append(exam_name)
		else:
			print("==== ERROR ====, Year and exam set does not match with each other")
	return result_dict

def getAvaliableFilters():
	return {"Overall": 0, "Institute Branch wise": 1, "Institute Branch CPI wise": 2,
			"Institute Subject wise": 3}

def getAllInstitute():
	result_dict = {}
	institutes = Result.objects.values_list("instcode", "instName")
	inst_set = set(institutes)
	print("Successfully fetch institutes!")
	for inst in inst_set:
		code, name = inst
		result_dict[name] = code
	return result_dict

def validateFilterData(data):
	if (data["year"] == "" or data["branch"] == "" or data["criteria"] == "" or
		data["year"] == None or data["branch"] == None or data["criteria"] == None):
		return "Select proper choice"

def doOverallFilter(year, branch):
	# Pass, Fail, Total, Percentage
	filter_data = {}
	columns = ["Sr. No.","Enrollment No.","Name", "Institute Name", "Institute Code", "Branch Code", "Branch Name",
			   "SPI", "CPI", "CGPA", "RESULT"]
	chart1_coulmn_data = OrderedDict()
	chart2_coulmn_data = OrderedDict()
	try:
		results = Result.objects.filter(AcademicYear=year, exam=branch).only(
			  "MAP_NUMBER", "name", "instcode", "instName", "BR_CODE", "BR_NAME",
			  "SPI", "CPI", "CGPA", "RESULT").order_by("-CPI")
		rows = {}
		i = 0;
		chart1_title = "Overall institutes result"
		chart2_title = "Overall branches result"
		chart_data = {}
		chart1_row_data = []
		chart2_row_data = []
		for result in results:
			rows[i] = {}
			rows[i]["Sr. No."] = i+1
			rows[i]["Enrollment No."] = result.MAP_NUMBER
			rows[i]["Name"] = result.name
			rows[i]["Institute Name"] = result.instName
			rows[i]["Institute Code"] = result.instcode
			rows[i]["Branch Code"] = result.BR_CODE
			rows[i]["Branch Name"] = result.BR_NAME
			rows[i]["SPI"] = result.SPI
			rows[i]["CPI"] = result.CPI
			rows[i]["CGPA"] = result.CGPA
			rows[i]["RESULT"] = result.RESULT
			chart1_row_data.append([float(result.SPI), int(result.instcode)])
			chart2_row_data.append([float(result.SPI), int(result.BR_CODE)])
			i += 1

		chart1_coulmn_data["SPI"] = 'number'
		chart1_coulmn_data["Institute code"] = "number"
		chart2_coulmn_data["SPI"] = 'number'
		chart2_coulmn_data["Branch code"] = "number"
		chart_data[chart1_title] = {"column_data": chart1_coulmn_data,
									"row_data": chart1_row_data,
									"options": {"title": chart1_title},
									"type": "scatter"}
		chart_data[chart2_title] = {"column_data": chart2_coulmn_data,
									"row_data": chart2_row_data,
									"options": {"title": chart2_title},
									"type": "scatter"}
	except Result.DoesNotExist:
		rows = {}

	filter_data["All students result"] = {"row": rows, "column": columns, "chart_data": chart_data}
	return filter_data

def doInstituteBranchWiseFilter(year, branch, institute):
	# Pass, Fail, Total, Percentage
	filter_data = {}
	columns = ["Branch Code", "Branch Name", "Total", "Pass", "Fail", "Percentage"]
	chart_data = {}
	try:
		all_branches = Result.objects.filter(AcademicYear=year, exam=branch, instName=institute)
		no_of_branches = all_branches.values_list("BR_CODE", "BR_NAME").distinct().order_by("BR_NAME")

		rows = {}
		i = 0;
		for branch in no_of_branches:
			br_code, br_name = branch
			chart_row_data = []
			chart_coulmn_data = OrderedDict()
			rows[i] = {}
			rows[i]["Branch Code"] = br_code
			rows[i]["Branch Name"] = br_name

			results = all_branches.filter(BR_CODE=br_code, BR_NAME=br_name)

			rows[i]["Total"] = results.count()
			rows[i]["Pass"] = results.filter(RESULT="PASS").count()
			rows[i]["Fail"] = results.filter(RESULT="FAIL").count()

			chart_row_data = [["Pass", rows[i]["Pass"]], ["Fail", rows[i]["Fail"]]]
			chart_coulmn_data["Result"] = "string"
			chart_coulmn_data['No of student'] = "number"
			chart_data[br_name] = {}
			chart_data[br_name] = {"column_data": chart_coulmn_data,
							       "row_data": chart_row_data,
					               "options": {"title": br_name},
					               "type": "pie"}

			if rows[i]["Total"] is not 0:
				rows[i]["Percentage"] = round((rows[i]["Pass"]  * 100)/ rows[i]["Total"], 2);
			else:
				rows[i]["Percentage"] = 0
			i += 1
	except Result.DoesNotExist:
		rows = {}

	filter_data["Branch wise filter of institute"] = {"row": rows, "column": columns, "chart_data": chart_data}
	return filter_data

def doInstituteBranchCPIWiseFilter(year, branch, institute):
	# Pass, Fail, Total, Percentage
	filter_data = {}
	columns = ["Branch Code", "Branch Name", "Total", "CPI > 6", "CPI > 7", "CPI > 8", "CPI > 9"]
	chart_data = {}
	try:
		all_branches = Result.objects.filter(AcademicYear=year, exam=branch, instName=institute)
		no_of_branches = all_branches.values_list("BR_CODE", "BR_NAME").distinct().order_by("BR_NAME")

		rows = {}
		i = 0;
		for branch in no_of_branches:
			chart_row_data = []
			chart_coulmn_data = OrderedDict()
			br_code, br_name = branch
			rows[i] = {}
			rows[i]["Branch Code"] = br_code
			rows[i]["Branch Name"] = br_name

			results = all_branches.filter(BR_CODE=br_code, BR_NAME=br_name)

			rows[i]["Total"] = results.count()
			rows[i]["CPI > 6"] = results.filter(CPI__startswith='6').count()
			rows[i]["CPI > 7"] = results.filter(CPI__startswith='7').count()
			rows[i]["CPI > 8"] = results.filter(CPI__startswith='8').count()
			rows[i]["CPI > 9"] = results.filter(CPI__startswith='9').count()

			chart_row_data = [["CPI > 6", rows[i]["CPI > 6"]],
								  ["CPI > 7", rows[i]["CPI > 7"]],
								  ["CPI > 8", rows[i]["CPI > 8"]],
								  ["CPI > 9", rows[i]["CPI > 9"]]]
			chart_coulmn_data["CPI Result"] = "string"
			chart_coulmn_data['No of students'] = "number"
			chart_data[br_name] = {}
			chart_data[br_name] = {"column_data": chart_coulmn_data,
							       "row_data": chart_row_data,
					               "options": {"title": br_name},
					               "type": "pie"}
			i += 1

	except Result.DoesNotExist:
		rows = {}

	filter_data["Branch CPI wise filter of institute"] = {"row": rows, "column": columns,
														  "chart_data": chart_data}
	return filter_data

def doInstituteSubjectWiseFilter(year, branch, institute):
	# Pass, Fail, Total, Percentage
	filter_data = {}
	columns = ["Sr. No.","Subject Name", "Total", "Pass", "Fail", "Percentage"]
	chart_data = {}
	try:
		all_subjects = Result.objects.filter(AcademicYear=year, exam=branch, instName=institute)	
		rows = {}
		i = 0
		k = 1
		for j in range(1,9):
			sub = "SUB" + str(j) + "NA"
			no_of_subjects = all_subjects.values_list(sub).distinct()
			for subject in no_of_subjects:
				chart_row_data = []
				chart_coulmn_data = OrderedDict()
				subject_name, = subject
				if subject_name is not "":												
					rows[i] = {}
					rows[i]["Sr. No."] = k; 
					rows[i]["Subject Name"] = subject_name
					if j is 1:
						results = all_subjects.filter(SUB1NA=subject_name)
					if j is 2:
						results = all_subjects.filter(SUB2NA=subject_name)
					if j is 3:
						results = all_subjects.filter(SUB3NA=subject_name)
					if j is 4:
						results = all_subjects.filter(SUB4NA=subject_name)
					if j is 5:
						results = all_subjects.filter(SUB5NA=subject_name)
					if j is 6:
						results = all_subjects.filter(SUB6NA=subject_name)
					if j is 7:
						results = all_subjects.filter(SUB7NA=subject_name)
					if j is 8:
						results = all_subjects.filter(SUB8NA=subject_name)

					rows[i]["Total"] = results.count()
					rows[i]["Pass"] = results.filter(RESULT="PASS").count()
					rows[i]["Fail"] = results.filter(RESULT="FAIL").count()
					chart_row_data = [["Pass", rows[i]["Pass"]], ["Fail", rows[i]["Fail"]]]
					chart_coulmn_data["Result"] = "string"
					chart_coulmn_data['No of student'] = "number"
					chart_data[subject_name] = {}
					chart_data[subject_name] = {"column_data": chart_coulmn_data,
										       "row_data": chart_row_data,
								               "options": {"title": subject_name},
								               "type": "pie"}
					if rows[i]["Total"] is not 0:
						rows[i]["Percentage"] = round((rows[i]["Pass"]  * 100 )/ rows[i]["Total"], 2);
					else:
						print("Why ZERO")
						rows[i]["Percentage"] = 0
					i += 1
					k += 1
	except Result.DoesNotExist:
		rows = {}

	filter_data["Subject wise filter of institute"] = {"row": rows, "column": columns,
															  "chart_data": chart_data}
	return filter_data

def filterData(data):
	if data["criteria"] == "Overall":
		filter_data = doOverallFilter(data["year"], data["branch"])
	elif data["criteria"] == "Institute Branch wise":
		filter_data = doInstituteBranchWiseFilter(data["year"], data["branch"], data["institute"])
	elif data["criteria"] == "Institute Branch CPI wise":
		filter_data = doInstituteBranchCPIWiseFilter(data["year"], data["branch"], data["institute"])
	elif data["criteria"] == "Institute Subject wise":
		filter_data = doInstituteSubjectWiseFilter(data["year"], data["branch"], data["institute"])
	else:
		print("=== ERROR === unexpected criteria")
		return
	return filter_data

def FilterHomePage(request):
	result_data = {}
	data = {}

	print("Validating data...")
	data["year"] = request.GET.get('year', None)
	data["branch"] = request.GET.get('branch', None)
	data["criteria"] = request.GET.get('criteria', None)
	data["institute"] = request.GET.get('institute', None)

	response = validateFilterData(data)
	if (response is not None):
		result_data["error_msg"] = response
		return JsonResponse(result_data)

	print("Filtering data...")

	# Extract year first
	try:
		if "winter" in data["year"].lower():
			# given_year - (given_year + 1)
			temp = data["year"].split(" ")[1]
			temp = temp + "-" + str(int(temp) + 1)
		elif "summer" in data["year"].lower():
			# (given_year - 1) - given_year
			temp = data["year"].split(" ")[1]
			temp = str(int(temp) - 1) + "-" + temp
		else:
			print("=== ERROR === unwanted parameter in result session neither winter nor summer")
			return JsonResponse(result_data)
		data["year"] = temp
	except ValueError as ex:
		print("=== ERROR === unwanted parameter in result session, can not convert to number")
		return JsonResponse(result_data)

	print("Successfully get result year")

	# DO FILTER
	filter_data = filterData(data)
	print("Successfully filter data")
	result_data["result"] = filter_data

	return JsonResponse(result_data)

def HomePage(request):
	js_dropdown_data = json.dumps(getResultSession())
	js_filter_data = json.dumps(getAvaliableFilters())
	js_institute_data = json.dumps(getAllInstitute())
	return render(request, "home.html", {"dropdown_data": js_dropdown_data,
										 "filters": js_filter_data,
										 "institutes": js_institute_data})
