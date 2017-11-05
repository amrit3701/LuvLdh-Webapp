
from django.conf.urls import url

from . import views

from django.views.generic import TemplateView

urlpatterns = [
        #directs to index veiw
        url(r'^upload/$', views.upload, name='upload'),
]
