from django.urls.conf import path

from . import views

company_urlpatterns = [
    path("", views.VacancyListCreateAPIView.as_view(), name="company_vacancy_list"),
    path("<slug:slug>/", views.VacancyDetailAPIView.as_view(), name="company_vacancy_detail"),
    path("<slug:slug>/feedbacks/", views.FeedbackListCreateAPIView.as_view(), name="company_vacancy_feedback_list"),
]

candidate_urlpatterns = [
    path("feedbacks/", views.CandidateFeedbackListAPIView.as_view(), name="candidate_feedback_list"),
    path(
        "feedbacks/<int:pk>", views.CandidateFeedbackDetailAPIView.as_view(), name="candidate_feedback_detail"
    ),
]

urlpatterns = company_urlpatterns + candidate_urlpatterns
