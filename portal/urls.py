from django.contrib import admin
from django.urls import include, path
from .import views
urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('faq', views.faq, name="faq"),
    path('paper/<str:external_id>/<str:code>', views.paper, name="paper"),
    path('result/<str:external_id>/<str:code>', views.result, name="result"),
    path('check-result', views.check_result, name="check-result"),
    path('check-scores', views.check_scores, name="check-scores"),
]