from django.db import models
from django.contrib.auth.models import User


class TrainingModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название тренировки')
    description = models.TextField(verbose_name='Описание тренировки', blank=True, null=True)
    calories = models.PositiveSmallIntegerField(verbose_name='Калории')
    duration = models.PositiveSmallIntegerField(verbose_name='Длительность тренировки (мин)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    user = models.ForeignKey(User, related_name='trainings', verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'

class FoodModel(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название еды')
    description = models.TextField(verbose_name='Описание еды', blank=True, null=True)
    calories = models.PositiveSmallIntegerField(verbose_name='Калории')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    user = models.ForeignKey(User, related_name='foods', verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.role_name}"
    
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal_name}"
    
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    progress_percentage = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal.goal_name}: {self.progress_percentage}%"
    
    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'