from apps.accounts.api.permissions import CandidateRequiredPermission, RecruiterRequiredPermission
from apps.core import filters, pagination
from apps.vacancy.api.serializers import FeedbackSerializer, VacancySerializer
from apps.vacancy.models import Feedback, Vacancy, VacancyView
from django_filters import rest_framework as dj_filters
from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class VacancyListCreateAPIView(generics.ListCreateAPIView):
    """Vacancy List Create. Only recruiters can create new vacancies. Pagination page size is 15."""

    queryset = (
        Vacancy.objects.select_related("user", "company", "category", "user__recruiter_profile")
        .prefetch_related("skills", "vacancy_views", "feedback_vacancy")
        .all()
    )
    serializer_class = VacancySerializer
    pagination_class = pagination.MediumResultsSetPagination
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = filters.VacancyFilter

    def perform_create(self, serializer):
        user = self.request.user
        recruiter_profile = self.request.user.recruiter_profile
        if recruiter_profile.company:
            serializer.save(user=user, company=recruiter_profile.company)
        else:
            raise ValidationError({"error": "You do not have any company"})

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [RecruiterRequiredPermission]
        elif self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class VacancyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Vacancy Detail API. Only recruiters can update and delete vacancies."""

    queryset = Vacancy.objects.select_related("user", "company", "category").all()
    lookup_field = "slug"
    serializer_class = VacancySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [RecruiterRequiredPermission]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        user = request.user

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if user.is_authenticated and user.has_candidate_profile():
            viewer_ip = request.META.get("REMOTE_ADDR", None)
            # TODO: change when using only Docker and Celery Maybe
            VacancyView.record_view(vacancy=instance, user=user, viewer_ip=viewer_ip)
            # create_vacancy_view.delay(instance.id, user.id, viewer_ip)

        return Response(serializer.data)


class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    """Feedback List Create. Recruiter can GET feedback list of vacancy. Candidate can POST feedback.
    After creating feedback, is created ChatRoom and ChatMessage. Pagination page size is 10."""

    serializer_class = FeedbackSerializer
    lookup_field = "slug"
    pagination_class = pagination.MinimumResultsSetPagination

    def get_queryset(self):
        queryset = (
            Feedback.objects.select_related("user", "user__candidate_profile", "vacancy", "vacancy__company")
            .prefetch_related("contact_cv", "user__candidate_profile__skills", "user__candidate_profile__category")
            .filter(vacancy__slug=self.kwargs["slug"])
        )
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        vacancy = get_object_or_404(Vacancy, slug=self.kwargs["slug"])
        if Feedback.objects.filter(user=user, vacancy=vacancy).exists():
            raise serializers.ValidationError({"message": "Feedback already exists"})
        serializer.save(user=user, vacancy=vacancy, contact_cv=user.contact_cv)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [CandidateRequiredPermission]
        elif self.request.method == "GET":
            self.permission_classes = [RecruiterRequiredPermission]
        return super().get_permissions()


# class CandidateFeedbackListAPIView(generics.ListAPIView):
#     """Candidate Feedback List APIView. Only candidate can view self feedback."""
#
#     serializer_class = FeedbackSerializer
#     permission_classes = [CandidateRequiredPermission]
#
#     def get_queryset(self):
#         queryset = Feedback.objects.filter(user=self.request.user)
#         return queryset


# class CandidateFeedbackDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Candidate Feedback Detail APIView. Only candidate can edit or delete self feedback"""
#
#     serializer_class = FeedbackSerializer
#     permission_classes = [CandidateRequiredPermission]
#
#     def get_queryset(self):
#         queryset = Feedback.objects.filter(user=self.request.user)
#         return queryset
