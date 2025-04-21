from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index_view, name='home'),
    path('application', views.ApplicationView.as_view(), name='application'),
    path('my-application', views.my_application_view, name='my_application'),
    path('get-faculties/', views.get_faculties, name='get_faculties'),
    path('signup',views.signup_view, name='signup'),
    path('signin',views.signin_view, name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),

]