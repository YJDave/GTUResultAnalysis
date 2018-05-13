from django.conf.urls import url
from django.contrib import admin

from resultapp.views import (
	HomePage,
	FilterHomePage,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePage, name="home"),
    url(r'^filter/$', FilterHomePage, name="filter"),
]
