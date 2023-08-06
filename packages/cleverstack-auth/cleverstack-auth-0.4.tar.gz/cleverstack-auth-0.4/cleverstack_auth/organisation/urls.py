from django.urls import path
from rest_framework import routers
from django.conf.urls import include

from . import views

app_name = 'organisation'

router = routers.DefaultRouter()
# router.register('plan', views.OrganisationPlanViewSet, basename='org_package')
router.register('branch/department', views.DepartmentViewSet, basename='department')
router.register('branch', views.BranchViewSet, basename='branch')

urlpatterns = [
	path('', include(router.urls)),
]
