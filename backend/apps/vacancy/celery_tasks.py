# from apps.vacancy.models import VacancyView
# from celery import app
#
#
# @app.shared_task()
# def create_vacancy_view(vacancy_id, user_id, viewer_ip):
#     print(vacancy_id, user_id, viewer_ip)
#     view, _ = VacancyView.objects.get_or_create(
#         vacancy_id=vacancy_id,
#         user_id=user_id,
#         viewer_ip=viewer_ip,
#     )
#     view.save()
#
#     return "Vacancy View created successfully"
