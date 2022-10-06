from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('settings', views.settings, name='settings'),
    path('datenanalyse', views.dataanalysis, name='dataanalysis'),
    path('cameralivefeed', views.livecamera, name='cameralivefeed'),
    path('testapi', views.testapi, name="testapi")
]