from django.urls import path
from study_admin import views

# (?P<name>pattern)  正则表达式，分组并起名字
urlpatterns = [
    path('study-login.html/', views.login),
    path('study-index.html/', views.study_index),
]