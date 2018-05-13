from django.contrib.auth import views
from django.shortcuts import render, get_object_or_404, redirect
from .models import Result
from django.http import JsonResponse
import json
from django.core import serializers

def getResultSession():
	result_dict = {}

	years = Result.objects.values_list("AcademicYear", "exam")
	year_set = set(years)
	print("Successfully fetch years!")

	# Dropdown values for result year
	for year in year_set:
		temp = year[0].split("-")
		result_dict["Winter " + str(temp[0])] = []
		result_dict["Summer " + str(temp[1])] = []
		if temp[0] in year[1]:
			result_dict["Winter " + str(temp[0])].append(year[1])
		elif temp[1] in year[1]:
			result_dict["Summer " + str(temp[1])].append(year[1])
		else:
			print("==== ERROR ====, Year and exam set does not match with each other")
	return result_dict

def getAvaliableFilters():
	return {"Overall": 0, "Institute Branch wise": 1, "Institute Branch CPI wise": 2,
			"Institute Branch Gender wise": 3, "Institute Subject wise": 4}

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
	columns = ["Name", "Institute Name", "Institute Code", "Branch Code", "Branch Name",
			   "SPI", "CPI", "CGPA", "RESULT"]
	try:
		results = Result.objects.filter(AcademicYear=year, exam=branch).only(
			  "name", "instcode", "instName", "BR_CODE", "BR_NAME",
			  "SPI", "CPI", "CGPA", "RESULT")
		rows = {}
		i = 0;
		for result in results:
			rows[i] = {}
			rows[i]["Name"] = result.name
			rows[i]["Institute Name"] = result.instName
			rows[i]["Institute Code"] = result.instcode
			rows[i]["Branch Code"] = result.BR_CODE
			rows[i]["Branch Name"] = result.BR_NAME
			rows[i]["SPI"] = result.SPI
			rows[i]["CPI"] = result.CPI
			rows[i]["CGPA"] = result.CGPA
			rows[i]["RESULT"] = result.RESULT
			i += 1
	except Result.DoesNotExist:
		rows = {}

	filter_data["All students result"] = {"row": rows, "column": columns}
	return filter_data

def doInstituteBranchWiseFilter(year, branch, institute):
	# Pass, Fail, Total, Percentage
	filter_data = {}
	columns = ["Branch Code", "Branch Name", "Total", "Pass", "Fail", "Percentage"]
	try:
		all_branches = Result.objects.filter(AcademicYear=year, exam=branch, instName=institute)
		no_of_branches = all_branches.values_list("BR_CODE", "BR_NAME").distinct()

		rows = {}
		i = 0;
		for branch in no_of_branches:
			br_code, br_name = branch
			rows[i] = {}
			rows[i]["Branch Code"] = br_code
			rows[i]["Branch Name"] = br_name

			results = all_branches.filter(BR_CODE=br_code, BR_NAME=br_name)

			rows[i]["Total"] = results.count()
			rows[i]["Pass"] = results.filter(RESULT="PASS").count()
			rows[i]["Fail"] = results.filter(RESULT="FAIL").count()
			if rows[i]["Total"] is not 0:
				rows[i]["Percentage"] = round(rows[i]["Pass"] / rows[i]["Total"] * 100, 2);
			else:
				rows[i]["Percentage"] = 0
			i += 1
	except Result.DoesNotExist:
		rows = {}

	filter_data["Branch wise filter of institute"] = {"row": rows, "column": columns}
	return filter_data

def doInstituteBranchCPIWiseFilter(year, branch, institute):
	return

def doInstituteBranchGenderWiseFilter(year, branch, institute):
	return

def doInstituteSubjectWiseFilter(year, branch, institute):
	return

def filterData(data):
	if data["criteria"] == "Overall":
		filter_data = doOverallFilter(data["year"], data["branch"])
	elif data["criteria"] == "Institute Branch wise":
		filter_data = doInstituteBranchWiseFilter(data["year"], data["branch"], data["institute"])
	elif data["criteria"] == "Institute Branch CPI wise":
		filter_data = doInstituteBranchCPIWiseFilter(data["year"], data["branch"], data["institute"])
	elif data["criteria"] == "Institute Branch Gender wise":
		filter_data = doInstituteBranchGenderWiseFilter(data["year"], data["branch"], data["institute"])
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
