from django.contrib import admin

from .models import Result

class ResultAdmin(admin.ModelAdmin):
	list_display = ["St_Id", "extype", "examid", "exam", "DECLARATIONDATE",
					"AcademicYear", "sem", "name", "instcode", "instName",
					"CourseName", "BR_CODE", "BR_NAME", "SPI", "CPI", "CGPA", "RESULT"]
	class Meta:
		model = Result


admin.site.register(Result, ResultAdmin)
