# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2] - 2024-03-26

Here we would have the update steps for 0.2 for people to follow.

### Added

- CHANGELOG.md file.
- ConditionalGetMiddleware in middleware for optimize response.
- GZipMiddleware in middleware for compress response.

### Changed

- CandidateProfileListAPIView optimize queryset DB requests. n+1 there is no.
- RecruiterProfileListAPIView optimize, n+1 no.
- VacancyListCreateAPIView and VacancySerializer optimize. Nested serializer made unnecessary requests to the DB(n+1).
  Queryset too.
- VacancyDetailAPIView optimize retrieve(GET detail) and queryset.
- FeedbackListCreateAPIView optimize queryset.

### Fixed

- In RecruiterProfile model, field company add blank=True.
- MINOR Clean Code
