from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('blog/<int:pk>',views.blog,name='blogpage'),
    path('allblogs',views.allblogs,name='allblogs'),
    path('contact',views.contact,name='contact'),
]
