import django_filters
from apps.accounts.models import CandidateProfile, RecruiterProfile
from apps.other.models import Company
from apps.vacancy.models import Vacancy


class CandidateProfileFilter(django_filters.FilterSet):
    class Meta:
        model = CandidateProfile
        fields = {
            "category__id": ["exact"],
            "skills__name": ["exact"],
            "work_exp": ["gt", "lt", "range"],
            "salary_expectation": ["gt", "lt", "range"],
            "country": ["exact"],
            "eng_level": ["exact"],
            "find_job": ["exact"],
            # "employ_options": ['exact'],
        }


class RecruiterProfileFilter(django_filters.FilterSet):
    class Meta:
        model = RecruiterProfile
        fields = {
            "country": ["exact"],
            "company__id": ["exact"],
            "trust_hr": ["exact"],
        }


class VacancyFilter(django_filters.FilterSet):
    class Meta:
        model = Vacancy
        fields = {
            "company__id": ["exact"],
            "category__id": ["exact"],
            "user__recruiter_profile__trust_hr": ["exact"],
            "skills__name": ["exact"],
            "eng_level": ["exact"],
            "country": ["exact"],
            "salary": ["gt", "lt", "range"],
            "work_exp": ["gt", "lt", "range"],
            "is_only_ukraine": ["exact"],
            "is_test_task": ["exact"],
        }


class MyCompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = {
            "country": ["exact"],
        }
