from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('signin/', views.sign_in),
    path('signup/', views.sign_up),
    path('editprofile/', views.edit_profile),
    path('changepassword/', views.change_password),
    path('signout/', views.sign_out),
    path('requestloan/', views.request_loan),
    path('createnewprofile/', views.create_new_profile),
    path('profiledetails/<int:id>/', views.profile_details),
    path('editstaff/<int:id>/', views.edit_staff),
    path('deletestaff/<int:id>/', views.delete_staff),
    path('deletefile/<int:id>/', views.delete_file),
    path('editfile/<int:id>/', views.edit_file),
    path('createnewfile/<int:id>/', views.create_new_file)
]