from django.contrib import admin
from django.urls import include, path
from .import views
urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('faq', views.faq, name="faq"),
    path('paper/<str:id>/<str:code>', views.paper, name="paper"),
    path('result/<str:id>/<str:code>', views.result, name="result"),
    path('check-result', views.check_result, name="check-result"),
]