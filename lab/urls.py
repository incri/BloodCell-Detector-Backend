from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()

router.register("blood-tests", views.BloodTestViewSet)
router.register("patients", views.PatientViewSet)

blood_tests_router = routers.NestedDefaultRouter(
    router, "blood-tests", lookup="blood_test"
)
patients_router = routers.NestedDefaultRouter(router, "patients", lookup="patient")

blood_tests_router.register(
    "results", views.ResultViewSet, basename="blood-test-results"
)
patients_router.register("address", views.AddressViewSet, basename="patient-address")

urlpatterns = router.urls + patients_router.urls + blood_tests_router.urls
