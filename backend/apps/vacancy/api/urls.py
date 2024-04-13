from django.urls.conf import path

from . import views

urlpatterns = [
    path("", views.VacancyListAPIView.as_view(), name="vacancy_list"),
    path("my/", views.VacancyMyListCreateAPIView.as_view(), name="vacancy_my_list"),
    path("my/<slug:slug>/", views.VacancyMyDetailAPIView.as_view(), name="vacancy_my_detail"),
    path("<slug:slug>/", views.VacancyDetailAPIView.as_view(), name="vacancy_detail"),
    path("<slug:slug>/feedbacks/", views.FeedbackListCreateAPIView.as_view(), name="vacancy_feedback_list"),
]
