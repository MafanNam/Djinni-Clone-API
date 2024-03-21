from django.urls.conf import path

from . import views

urlpatterns = [
    path("", views.VacancyListCreateAPIView.as_view()),
    path("feedback/", views.CandidateFeedbackListAPIView.as_view()),
    path("feedback/<int:pk>", views.CandidateFeedbackDetailAPIView.as_view()),
    path("<slug>/", views.VacancyDetailAPIView.as_view()),
    path("<slug>/feedback/", views.FeedbackListCreateAPIView.as_view()),
]
