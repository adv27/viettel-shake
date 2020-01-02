from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import index_template_view, viettel_user_detail_view
from .viewsets import ViettelShakeViewSet, ViettelUserViewSet

app_name = 'shake'

router = DefaultRouter()
router.register(r'shake', ViettelShakeViewSet, basename='shake')
router.register(r'user', ViettelUserViewSet, basename='user')

urlpatterns = [
    path('', index_template_view, name='index'),
    path('detail/<str:phone>/', viettel_user_detail_view),
]
urlpatterns += router.urls
