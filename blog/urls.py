from django.urls import path
from blog import views

urlpatterns = [
    path('cur_time/', views.cur_time ),
    path('userInfo/', views.userInfo),
    path('articles/2003/', views.special_case_2003),    # 完全匹配
    path('articles/<int:year>/<int:month>/', views.year_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
    path('index/', views.index, {'name': "charley"}),
    # http://127.0.0.1:8000/blog/index_rename/
    path('index_rename/', views.index_rename, name='newName'),  # 让URL可以更改
    path('login/', views.login),
    path("homepage/", views.homepage),
    path('index_template/', views.index_template),
    path('ordered/', views.ordered),
    path('shoppingcart/', views.shoppingcart),
    path('data_operation/', views.data_operation),
    path('ajax_test/', views.ajax_test),
    path('ajax_receive/', views.ajax_receive),
    path('register/', views.register),
    path('jquery_test/', views.jquery_test),
    path('jquery_html/', views.jquery_html),
]
