# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [0.3] - 2024-03-28

### Added

-

### Changed

-

### Fixed

-


## [0.2] - 2024-03-26

### Added

- CHANGELOG.md file.
- ConditionalGetMiddleware in middleware for optimize response.
- GZipMiddleware in middleware for compress response.
- Pagination for all GET list url(uri)
- Django-filter, custom filters for profile and vacancy.
- Search in vacancy
- Ordering in vacancy and by trust_hr
- Default model image for Profile, Company
- Fixtures for user
- Nginx container and config
- Celery beat schedule task spam-mail-every-week
- Subscribe to spam email url, view

### Changed

- CandidateProfileListAPIView optimize queryset DB requests. n+1 there is no.
- RecruiterProfileListAPIView optimize, n+1 no.
- VacancyListCreateAPIView and VacancySerializer optimize. Nested serializer made unnecessary requests to the DB(n+1).
  Queryset too.
- VacancyDetailAPIView optimize retrieve(GET detail) and queryset.
- FeedbackListCreateAPIView optimize queryset.
- Activation email template

### Fixed

- In RecruiterProfile model, field company add blank=True.
- MINOR Clean Code.
- Ordering chat model and message
- Improve Dockerfile
- CustomTokenObtainPairView bug and refactor
