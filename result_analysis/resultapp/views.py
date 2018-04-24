from django.contrib.auth import views

class HomePage(views.TemplateView):
    template_name = "home.html"
    pass
