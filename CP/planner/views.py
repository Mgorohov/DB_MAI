from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.contrib import messages
from django.urls import reverse

from .forms import RegisterForm, TrainingForm, FoodForm
from .models import TrainingModel, FoodModel

def chart_data(user: User):
    with connection.cursor() as cursor:
        # Получаем данные о тренировках для текущего пользователя
        cursor.execute("""
            SELECT DATE(created_at) AS date, COUNT(id) AS count
            FROM planner_trainingmodel
            WHERE user_id = %s
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """, [user.id])
        trainings = cursor.fetchall()
        training_dates = [datetime.strptime(str(item[0]), '%Y-%m-%d').strftime('%Y-%m-%d') for item in trainings]
        training_counts = [item[1] for item in trainings]

        # Получаем данные о приемах пищи для текущего пользователя
        cursor.execute("""
            SELECT DATE(created_at) AS date, SUM(calories) AS total_calories
            FROM planner_foodmodel
            WHERE user_id = %s
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """, [user.id])
        foods = cursor.fetchall()
        food_dates = [datetime.strptime(str(item[0]), '%Y-%m-%d').strftime('%Y-%m-%d') for item in foods]
        food_calories = [item[1] for item in foods]

        # Получаем данные о тренировках для калорий для текущего пользователя
        cursor.execute("""
            SELECT DATE(created_at) AS date, SUM(calories) AS total_calories
            FROM planner_trainingmodel
            WHERE user_id = %s
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
        """, [user.id])
        training_calories = cursor.fetchall()
        training_cal_dates = [datetime.strptime(str(item[0]), '%Y-%m-%d').strftime('%Y-%m-%d') for item in training_calories]
        training_cal_calories = [item[1] for item in training_calories]

    # Объединяем данные о тренировках и приемах пищи
    combined_dates = set(food_dates + training_cal_dates)
    combined_dates = sorted(list(combined_dates))

    net_calories = []
    for date in combined_dates:
        training_cal = next((cal for d, cal in zip(training_cal_dates, training_cal_calories) if d == date), 0)
        food_cal = next((cal for d, cal in zip(food_dates, food_calories) if d == date), 0)
        net_calories.append(food_cal - training_cal)

    context = {
        'training_dates': training_dates,
        'training_counts': training_counts,
        'combined_dates': combined_dates,
        'net_calories': net_calories,
    }

    return context

class RegisterView(View):
    def get(self, request: HttpRequest):
        regform = RegisterForm(request.POST)
        return render(
            request,
            "registration/registration.html",
            {'regform': regform}
        )

    def post(self, request: HttpRequest):
        regform = RegisterForm(request.POST)
        if regform.is_valid():
            regform.save()
            return redirect(reverse('login'))
        else:
            messages.error(
                request,
                'Ошибка при регистрации. Проверьте введенные данные.'
            )
            return render(
                request,
                "registration/registration.html",
                {'regform': regform}
            )


class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        return render(request, "registration/profile.html", context=chart_data(user=request.user))
    


class TrainingView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int = None):
        with connection.cursor() as cursor:
            if pk is None:
                cursor.execute("""
                    SELECT id, title, description, calories, duration, created_at
                    FROM planner_trainingmodel
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, [request.user.id])
                trainings = cursor.fetchall()
                trainings = [TrainingModel(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    calories=row[3],
                    duration=row[4],
                    created_at=row[5],
                    user=request.user
                ) for row in trainings]
                return render(request, 'planner/training-page.html', {'trainings': trainings, 'form': TrainingForm()})
            else:
                cursor.execute("""
                    SELECT id, title, description, calories, duration, created_at
                    FROM planner_trainingmodel
                    WHERE id = %s AND user_id = %s
                """, [pk, request.user.id])
                training = cursor.fetchone()
                if training:
                    training = TrainingModel(
                        id=training[0],
                        title=training[1],
                        description=training[2],
                        calories=training[3],
                        duration=training[4],
                        created_at=training[5],
                        user=request.user
                    )
                    return render(request, 'planner/training-detail-page.html', {'training': training, 'form': TrainingForm(instance=training)})
                else:
                    return redirect(reverse('trainings'))
                

    def post(self, request: HttpRequest, pk: int = None):
        if pk is None:
            
            training_form = TrainingForm(request.POST)
            
            if training_form.is_valid():
                training: TrainingModel = training_form.save(commit=False)
                training.user = request.user
                training.save()
                return redirect(reverse('trainings'))
            else:
                messages.error(
                    request,
                    'Ошибка при заполнении формы. Проверьте введенные данные.'
                )
                return redirect(reverse('trainings'))
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM planner_trainingmodel
                    WHERE id = %s AND user_id = %s
                """, [pk, request.user.id])
                training = cursor.fetchone()
                
                if training:
                    
                    training = TrainingModel(
                        id=training[0],
                        title=training[1],
                        description=training[2],
                        calories=training[3],
                        duration=training[4],
                        created_at=training[5],
                        user=request.user
                    )
                    form = TrainingForm(request.POST, instance=training)
                    if form.is_valid():
                        form.save()
                        return redirect(reverse('trainings', args=[pk]))
                    else:
                        messages.error(
                            request,
                            'Ошибка при заполнении формы. Проверьте введенные данные.'
                        )
                        return redirect(reverse('trainings'))
                else:
                    return redirect(reverse('trainings'))

    def delete(self, request: HttpRequest, pk: int):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM planner_trainingmodel
                WHERE id = %s AND user_id = %s
            """, [pk, request.user.id])
        return JsonResponse({"status": "success"})


class MealRecordView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int = None):
        with connection.cursor() as cursor:
            if pk is None:
                cursor.execute("""
                    SELECT * FROM planner_foodmodel
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                """, [request.user.id])
                foods = cursor.fetchall()
                foods = [FoodModel(
                        id=row[0],
                        title=row[1],
                        description=row[2],
                        calories=row[6],
                        created_at=row[4],
                        user=request.user
                )
                    for row in foods
                ]
                return render(request, 'planner/food-page.html', {'foods': foods, 'form': FoodForm()})
            else:
                cursor.execute("""
                    SELECT * FROM planner_foodmodel
                    WHERE id = %s AND user_id = %s
                """, [pk, request.user.id])
                food = cursor.fetchone()
                if food:
                    print(food)
                    food = FoodModel(
                        id=food[0],
                        title=food[1],
                        description=food[2],
                        calories=food[6],
                        created_at=food[4],
                        user=request.user
                )
                    print(food)
                    return render(request, 'planner/food-detail-page.html', {'food': food, 'form': FoodForm(instance=food)})
                else:
                    return redirect(reverse('foods'))

    def post(self, request: HttpRequest, pk: int = None):
        if pk is None:
            food_form = FoodForm(request.POST)
            if food_form.is_valid():
                food: FoodModel = food_form.save(commit=False)
                food.user = request.user
                food.save()
                return redirect(reverse('foods'))
            else:
                messages.error(
                    request,
                    'Ошибка при заполнении формы. Проверьте введенные данные.'
                )
                return redirect(reverse('foods'))
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM planner_foodmodel
                    WHERE id = %s AND user_id = %s
                """, [pk, request.user.id])
                food = cursor.fetchone()
                if food:
                    food = FoodModel(
                        id=food[0],
                        title=food[1],
                        description=food[2],
                        calories=food[3],
                        created_at=food[4],
                        user=request.user
                    )
                    form = FoodForm(request.POST, instance=food)
                    if form.is_valid():
                        form.save()
                        return redirect(reverse('foods', args=[pk]))
                    else:
                        messages.error(
                            request,
                            'Ошибка при заполнении формы. Проверьте введенные данные.'
                        )
                        return redirect(reverse('foods'))
                else:
                    return redirect(reverse('foods'))

    def delete(self, request: HttpRequest, pk: int):
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM planner_foodmodel
                WHERE id = %s AND user_id = %s
            """, [pk, request.user.id])
        return JsonResponse({"status": "success"})
        

def main_page_view(request: HttpRequest):
    return render(request, 'planner/main-page.html')


