from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, upload_file

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('upload/', upload_file),
    path('', include(router.urls)),
]
