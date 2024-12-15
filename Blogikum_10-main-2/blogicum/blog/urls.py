from django.urls import path
from . import views

app_name = 'blog'  # Пространство имен для маршрутов приложения

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('post/add/', views.add_post, name='add_post'),  # Добавление поста
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # Редактирование поста
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Удаление поста
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),  # Посты категории
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # Маршрут для просмотра поста
    path('profile/<str:username>/', views.profile, name='profile'),  # Профиль пользователя
    path('about/', views.about, name='about'),  # Маршрут для "О проекте"
    path('rules/', views.rules, name='rules'),  # Маршрут для "Наши правила"
]
