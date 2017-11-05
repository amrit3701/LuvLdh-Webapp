
from django.conf.urls import url

from . import views

from django.views.generic import TemplateView

urlpatterns = [
        #directs to index veiw
        url(r'^upload_photo/$', views.upload_photo, name='upload_photo'),
        url(r'^upload_contentwriting/$', TemplateView.as_view(template_name='src/contentwriting.html')),
        url(r'^upload_contentwriting_postlink$', views.upload_contentwriting, name='upload_contentwriting'),
]
