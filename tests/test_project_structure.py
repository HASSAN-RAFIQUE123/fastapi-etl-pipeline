"""Regression tests for the new package-oriented application structure."""

from importlib import import_module


def test_new_application_modules_are_importable() -> None:
    """The refactored application packages should expose their modules cleanly."""
    modules = [
        "app.api.dependencies",
        "app.api.routers.customers",
        "app.api.routers.products",
        "app.api.routers.orders",
        "app.api.routers.payments",
        "app.api.routers.feedback",
        "app.services.customer_service",
        "app.repositories.customer_repository",
        "app.database.session",
        "app.schemas.customer",
        "app.core.constants",
        "app.middleware.request_logging",
        "app.exceptions.handlers",
        "app.utils.validators",
    ]

    for module_name in modules:
        module = import_module(module_name)
        assert module is not None
