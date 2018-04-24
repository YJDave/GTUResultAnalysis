from django.contrib.auth import views
from django.shortcuts import render, get_object_or_404, redirect
from .models import Result


# class HomePage(views.TemplateView):
# 	# rs = Result.objects.all()
#     template_name = "home.html"
#     pass

def HomePage(request):
	column = ["sem", "name", "instcode", "instName", "BR_CODE", "BR_NAME",
					"SPI", "CPI", "CGPA", "RESULT"]

	row = Result.objects.all()
	return render(request, "home.html", {"column": column, "row": row})
