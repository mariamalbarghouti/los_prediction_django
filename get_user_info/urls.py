from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prediction', views.submit_form, name='submit_form'),

]
