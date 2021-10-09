from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('signup', views.signup, name = 'signup'),
    path('signin', views.signin, name = 'signin'),
    path('mypage/<int:pk>', views.mypage, name = 'mypage'),
    path('create/<int:pk>', views.create, name = 'create'),
    path('delete/<int:num>/<int:pk>', views.delete, name = 'delete'),
    path('edit/<int:num>/<int:pk>', views.edit, name = 'edit'),  
]