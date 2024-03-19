from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryListAPIView.as_view()),
    path("companies/", views.CompanyListAPIView.as_view()),
]
