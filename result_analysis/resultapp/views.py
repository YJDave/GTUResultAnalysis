from django.contrib.auth import views
from django.shortcuts import render, get_object_or_404, redirect
from .models import Result
# from django.utils import simplejson
import json

def fillDropdown():
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

def HomePage(request):
	column = ["sem", "name", "instcode", "instName", "BR_CODE", "BR_NAME",
					"SPI", "CPI", "CGPA", "RESULT"]

	js_dropdown_data = json.dumps(fillDropdown())
	js_filter_data = json.dumps(getAvaliableFilters())
	return render(request, "home.html", {"dropdown_data": js_dropdown_data,
										 "filters": js_filter_data})
