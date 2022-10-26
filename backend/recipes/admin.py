from django.contrib import admin

from .models import (Ingredient, IngredientRecipe, Recipe, Tag,
                     TagRecipe, ShoppingCart, Favorite)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        TagRecipeInline,
        IngredientRecipeInline,
    ]


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(TagRecipe)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
