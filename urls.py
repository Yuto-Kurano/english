from django.urls import path
from . import views
from django_app import settings


urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup, name = 'signup'),
    path('signin', views.signin, name = 'signin'),
    path('mypage/<int:pk>', views.mypage, name = 'mypage'),
    path('create/<int:pk>', views.create, name = 'create'),
    path('create_myself/<int:pk>', views.create_myself, name = 'create_myself'),
    path('delete/<int:num>/<int:pk>', views.delete, name = 'delete'),
    path('edit/<int:num>/<int:pk>', views.edit, name = 'edit'),  
    path('search/<int:pk>', views.search, name = 'search'),
    path('signout/<int:pk>', views.signout, name = 'signout'),
    path('user_delete/<int:pk>', views.user_delete, name = 'user_delete'),
    path('count/<int:pk>', views.count, name = 'count'),
    path('twitter/<int:pk>', views.twitter, name = 'twitter'),
]