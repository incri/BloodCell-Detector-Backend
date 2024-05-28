from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

# Define the default router
router = routers.DefaultRouter()

# Register the main endpoints
router.register("blood-tests", views.BloodTestViewSet, basename="blood-test")
router.register("patients", views.PatientViewSet,  basename="patient")

# Create nested routers
blood_tests_router = routers.NestedDefaultRouter(
    router, "blood-tests", lookup="blood_test"
)

patients_router = routers.NestedDefaultRouter(router, "patients", lookup="patient")

# Register nested resources
blood_tests_router.register(
    "results", views.ResultViewSet, basename="blood-test-results"
)

# Create a nested router for blood test results
results_router = routers.NestedDefaultRouter(
    blood_tests_router, "results", lookup="result"
)

# Register the results images endpoint
results_router.register(
    "result-images", views.ResultImageDataViewSet, basename="result-results-images"
)

# Register the patient address endpoint
patients_router.register("address", views.AddressViewSet, basename="patient-address")

blood_tests_router.register(
    "data-images", views.BloodTestImageDataViewSet, basename="image-data"
)


# Combine all URLs
urlpatterns = (
    router.urls + patients_router.urls + blood_tests_router.urls + results_router.urls
)
