from django.urls.conf import path

from . import views

urlpatterns = [
    path("", views.VacancyListCreateAPIView.as_view(), name="vacancy_list"),
    path("candidate/feedbacks/", views.CandidateFeedbackListAPIView.as_view(), name="candidate_feedback"),
    path(
        "candidate/feedbacks/<int:pk>", views.CandidateFeedbackDetailAPIView.as_view(), name="candidate_feedback_detail"
    ),
    path("<slug:slug>/", views.VacancyDetailAPIView.as_view(), name="vacancy_detail"),
    path("<slug:slug>/feedbacks/", views.FeedbackListCreateAPIView.as_view(), name="vacancy_feedback_list"),
]
