from django.contrib.auth import views

class HomePage(views.TemplateView):
	# rs = Result.objects.all()
    template_name = "home.html"
    pass
