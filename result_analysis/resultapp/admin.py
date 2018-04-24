from django.contrib import admin

from .models import Result

class ResultAdmin(admin.ModelAdmin):
	list_display = ["St_Id", "extype", "examid", "exam", "DECLARATIONDATE",
					"AcademicYear", "sem", "name", "instcode", "instName",
					"CourseName"]
	class Meta:
		model = Result


admin.site.register(Result, ResultAdmin)
