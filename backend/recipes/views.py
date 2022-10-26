from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from backend.settings import FOODGRAM, SHOPPING_CART

from .filters import IngredientSearchFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)
from .pagination import RecipePagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_serializer_class(self):
        """разделяет типы запросов на списковые и одиночные"""
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeWriteSerializer

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """добавляет или удаляет рецепт в избранном"""
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = FavoriteRecipeSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                Favorite, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """добавляет или удаляет рецепт в корзине"""
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': pk}
            serializer = ShoppingCartSerializer(
                data=data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, id=pk)
            favorite = get_object_or_404(
                ShoppingCart, user=user, recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """скачивает список ингридиентов из рецептов в корзине"""
        shopping_dict = {}
        ingredients = IngredientRecipe.objects.filter(
            recipe__in=request.user.shopping_cart.values('recipe')
        ).select_related('ingredient')
        for obj in ingredients:
            ingredient = obj.ingredient.name
            if ingredient not in shopping_dict:
                shopping_dict[ingredient] = {
                    'measurement_unit': obj.ingredient.measurement_unit,
                    'amount': obj.amount
                }
            else:
                shopping_dict[ingredient]['amount'] += obj.amount
        download_cart = SHOPPING_CART.format(username=request.user.username)
        for ingredient in shopping_dict:
            download_cart += (
                f'{ingredient} '
                f'({shopping_dict[ingredient]["measurement_unit"]}) '
                f'- {shopping_dict[ingredient]["amount"]}\n'
            )
        download_cart += FOODGRAM
        response = HttpResponse(
            download_cart,
            content_type='text/plain;charset=UTF-8',
        )
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_cart.txt"'
        )
        return response
