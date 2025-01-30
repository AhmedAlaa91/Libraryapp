from django.shortcuts import render
from rest_framework import  viewsets, permissions, status
from django.db.models import Q
from .models import Author, Book, Favorite 
from django.contrib.auth.models import User
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        if search_query:
            return Book.objects.filter(Q(title__icontains=search_query) |Q(genre__icontains=search_query) | Q(author__name__icontains=search_query))
        return super().get_queryset()

class FavoriteViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        userinstance = User.objects.filter(id=request.user.id).first()
        favorites = Favorite.objects.filter(user=userinstance)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book'],
            properties={
                'book': openapi.Schema(type=openapi.TYPE_INTEGER, description="Book ID to add to favorites")
            }
        ),
        responses={201: FavoriteSerializer}
    )

    def create(self, request):
        userinstance = User.objects.filter(id=request.user.id).first()
        if Favorite.objects.filter(user=userinstance).count() >= 20:
            return Response({"error": "Cannot have more than 20 favorites."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=userinstance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        userinstance = User.objects.filter(id=request.user.id).first()
        favorite = Favorite.objects.filter(user=userinstance, pk=pk).first()
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='recommendations')
    def recommendations(self, request):
        userinstance = User.objects.filter(id=request.user.id).first()
        user_favorites = Favorite.objects.filter(user=userinstance).values_list('book__id', flat=True)
        similar_books = Book.objects.exclude(id__in=user_favorites).order_by('-ratings')[:5] # Dummy similarity logic
        serializer = BookSerializer(similar_books, many=True)
        return Response(serializer.data)

