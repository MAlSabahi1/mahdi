"""
Base ViewSet Classes - الفئات الأساسية لجميع الـ ViewSets
توفر: StandardResponseMixin + IdempotencyMixin + DRF ViewSets
"""
from rest_framework import viewsets
from .mixins import StandardResponseMixin
from infra.security.idempotency import IdempotencyMixin


class BaseModelViewSet(StandardResponseMixin, IdempotencyMixin, viewsets.ModelViewSet):
    """Base class for full CRUD ViewSets with unified responses and idempotency."""
    pass


class BaseReadOnlyViewSet(StandardResponseMixin, viewsets.ReadOnlyModelViewSet):
    """Base class for read-only ViewSets with unified responses."""
    pass


class BaseViewSet(StandardResponseMixin, viewsets.ViewSet):
    """Base class for custom ViewSets with unified responses."""
    pass
