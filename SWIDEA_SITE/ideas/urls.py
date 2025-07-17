from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.idea_search, name='idea_search'),
    path('create/', views.create_idea, name='create_idea'),
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('idea/<int:pk>/edit/', views.idea_update, name='idea_update'),
    path('idea/<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('idea/<int:pk>/star/', views.toggle_star, name='toggle_star'),
    path('idea/<int:pk>/interest/', views.adjust_interest, name='adjust_interest'),
    path('devtools/', views.devtool_list, name='devtool_list'),
    path('devtools/create/', views.devtool_create, name='devtool_create'),
    path('devtools/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtools/<int:pk>/edit/', views.devtool_update, name='devtool_update'),
    path('devtools/<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),
] 