from django.conf.urls import url, include
from rest_framework import routers

from savant.resources.comparison import ComparisonViewSet
from savant.resources.diff import DiffViewSet
from savant.resources.set import SetViewSet

router = routers.DefaultRouter()
router.register(r'comparisons', ComparisonViewSet)
router.register(r'diffs', DiffViewSet)
router.register(r'sets', SetViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
