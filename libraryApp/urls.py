
from rest_framework.routers import DefaultRouter
from .views import * 
from django.urls import path, include
# URLs
router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
]