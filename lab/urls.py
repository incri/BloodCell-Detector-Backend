from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.conf import settings
from django.conf.urls.static import static
from . import views

# Define the default router
router = routers.DefaultRouter()

# Register the main endpoints
router.register("hospitals", views.HospitalViewSet, basename="hospital")


# Create nested routers


hospital_router = routers.NestedDefaultRouter(router, "hospitals", lookup="hospital")

hospital_router.register("patients", views.PatientViewSet, basename="patients")

patients_router = routers.NestedDefaultRouter(
    hospital_router, "patients", lookup="patient"
)

patients_router.register("address", views.AddressViewSet, basename="addresss")

patients_router.register("blood-tests", views.BloodTestViewSet, basename="blood-tests")

blood_test_router = routers.NestedDefaultRouter(
    patients_router, "blood-tests", lookup="blood_tests"
)

blood_test_router.register(
    "data-images", views.BloodTestImageDataViewSet, basename="image-data"
)

blood_test_router.register(
    "results", views.ResultViewSet, basename="blood-test-results"
)

results_router = routers.NestedDefaultRouter(
    blood_test_router, "results", lookup="result"
)

results_router.register(
    "result-images", views.ResultImageDataViewSet, basename="result-results-images"
)

urlpatterns = (
    router.urls
    + hospital_router.urls
    + patients_router.urls
    + blood_test_router.urls
    + results_router.urls
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
