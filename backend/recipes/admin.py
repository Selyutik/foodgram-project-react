from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag, TagRecipe)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1
    extra = 2


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'total_favorited')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author__username', 'tags__name')
    inlines = [
        IngredientRecipeInline,
        TagRecipeInline
    ]

    def total_favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Favorite, FavoriteAdmin)
