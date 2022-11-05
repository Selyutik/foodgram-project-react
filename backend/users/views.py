from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.pagination import LimitPageNumberPaginator
from .models import Follow, User
from .serializers import FollowSerializer, UserFollowSerializer


class FollowListAPIView(generics.ListAPIView):
    pagination_class = LimitPageNumberPaginator
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class UserFollowApiView(views.APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        data = {'user': request.user.id, 'author': id}
        serializer = UserFollowSerializer(
            data=data,  # type: ignore
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        follow = get_object_or_404(
            Follow, user=user, author=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
