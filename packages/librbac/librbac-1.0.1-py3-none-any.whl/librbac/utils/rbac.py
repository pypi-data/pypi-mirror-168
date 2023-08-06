from importlib import import_module
from typing import Generator
from typing import Set
from typing import Type

from django.conf import settings
from rest_framework.viewsets import GenericViewSet


def get_all_viewsets(
    urlpatterns,
    viewsets=None
) -> Set[Type[GenericViewSet]]:
    """Находит и возвращает все ViewSet'ы системы."""
    viewsets = viewsets if viewsets is not None else set()
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            get_all_viewsets(pattern.url_patterns, viewsets=viewsets)
        else:
            if cls := getattr(pattern.callback, 'cls', None):
                if issubclass(cls, GenericViewSet):
                    viewsets.add(cls)

    return viewsets


def _get_rbac_viewsets() -> Generator[GenericViewSet, None, None]:
    """Возвращает ViewSet'ы системы, доступ к которым нужно проверять."""
    from librbac.drf.viewsets import RBACMixin
    urlpatterns = import_module(settings.ROOT_URLCONF).urlpatterns
    for viewset in get_all_viewsets(urlpatterns):
        if issubclass(viewset, RBACMixin):
            yield viewset
