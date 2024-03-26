from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryListAPIView.as_view()),
    path("companies/", views.CompanyListCreateAPIView.as_view()),
    path("companies/<int:pk>", views.CompanyDetailAPIView.as_view()),
    path("skills/", views.SkillsListAPIView.as_view()),
]
