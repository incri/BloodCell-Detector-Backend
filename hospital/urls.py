from rest_framework_nested import routers
from . import views

# Define the default router
router = routers.DefaultRouter()



router.register("create", views.HospitalViewSet)



# Combine all URLs
urlpatterns = (
    router.urls)