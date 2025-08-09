# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-08-09

### Added

- Initial project setup for OSPO-ColabAchievements.
- Backend API with FastAPI, SQLModel, and SQLite for managing contributors and achievements.
- Worker script to fetch contributions (PRs, issues, commits) from GitHub and populate the database.
- Frontend UI with React and Vite for searching and displaying contributor achievements.
- Basic project structure, `README.md`, and `CHANGELOG.md`.
- CORS configuration for frontend-backend communication.
- Idempotent achievement creation in worker to prevent duplicates.
- Support for processing contributions from specific repositories or entire GitHub organizations.
