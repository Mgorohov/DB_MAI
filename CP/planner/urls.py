from .views import main_page_view, TrainingView, MealRecordView
from django.urls import path


urlpatterns = [
    path('', main_page_view, name='main-page'),
    path('trainings', TrainingView.as_view(), name='trainings'),
    path('trainings/<int:pk>', TrainingView.as_view(), name='trainings'),
    path('foods', MealRecordView.as_view(), name='foods'),
    path('foods/<int:pk>', MealRecordView.as_view(), name='foods'),
]
