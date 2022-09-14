from rest_framework import mixins, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    """Create view set."""
    pass


class RetrievePatchViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    """Retrieve and update view set."""
    pass


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    """List, create and destroy view set."""
    pass
