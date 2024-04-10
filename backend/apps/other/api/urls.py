from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryListAPIView.as_view()),
    path("companies/", views.CompanyListAPIView.as_view()),
    path("companies/<int:pk>/", views.CompanyDetailAPIView.as_view()),
    path("companies/my/", views.CompanyMyListCreateAPIView.as_view()),
    path("companies/my/<int:pk>/", views.CompanyMyDetailAPIView.as_view()),
    path("skills/", views.SkillsListAPIView.as_view()),
]
