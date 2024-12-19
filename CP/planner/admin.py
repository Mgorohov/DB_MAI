from django.contrib import admin

from .models import FoodModel, TrainingModel


@admin.register(FoodModel)
class FoodModelAdmin(admin.ModelAdmin):
    ...


@admin.register(TrainingModel)
class TrainingModelAdmin(admin.ModelAdmin):
    ...