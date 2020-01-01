from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import index_template_view, viettel_user_detail_view
from .viewsets import ViettelShakeViewSet

app_name = 'shake'

router = DefaultRouter()
router.register(r'shake', ViettelShakeViewSet, basename='shake')

urlpatterns = [
    path('', index_template_view),
    path('detail/<str:phone>', viettel_user_detail_view),
]
urlpatterns += router.urls
