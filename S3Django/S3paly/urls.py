from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'', views.index, name='home'),
    url(r'upload/', views.DocumentCreateView.as_view(template_name='document_form.html'), name='upload')
]