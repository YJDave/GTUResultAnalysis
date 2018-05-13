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
	try:
		row = serializers.serialize("json", Result.objects.filter(AcademicYear=year, exam=branch).only(
			  "sem", "name", "instcode", "instName", "BR_CODE", "BR_NAME",
			  "SPI", "CPI", "CGPA", "RESULT"),
			  fields=("sem", "name", "instcode", "instName", "BR_CODE", "BR_NAME",
			  "SPI", "CPI", "CGPA", "RESULT"))
	except Result.DoesNotExist:
		row = {}
	column = ["sem", "name", "instcode", "instName", "BR_CODE", "BR_NAME",
			  "SPI", "CPI", "CGPA", "RESULT"]
	filter_data["All students result"] = {"row": row, "column": column}
	return filter_data

def doInstituteBranchWiseFilter(year, branch, institute):
	return

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
