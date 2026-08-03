# Architecture

This project now follows a simple layered structure for the FastAPI application:

- app/api contains routers and shared dependencies.
- app/services hosts business logic.
- app/repositories manages persistence access.
- app/database keeps the ORM models and engine setup.
- app/schemas defines request and response payloads.
- app/core, app/middleware, app/exceptions, and app/utils hold cross-cutting helpers.

The ETL flow is split into extraction, transformation, and loading modules under the etl package.
