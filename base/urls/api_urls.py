from django.urls import path
from .api import *

urlpatterns = [



    path('categories/create/', CategoryCreateView.as_view(), name = "make-categories"),

    path('budget/create/', BudgetCreateView.as_view(), name='budget-create'),
    path('income/', IncomeCreateView.as_view(), name='income-create'),
    path('income/list/', UserIncomeListView.as_view(), name='user-income-list'),
    path('savings/', UserSavingsListView.as_view(), name='user-savings-list'),
    path('savings/<int:pk>/', UserSavingsDetailView.as_view(), name='user-savings-detail'),

    path('income/<str:pk>/', UserIncomeDetailView.as_view(), name='user-income-detail'),
    path('budget/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('savings/<int:pk>/delete/', SavingsDeleteView.as_view(), name='savings-delete'),
    path('savings/<int:pk>/update/', SavingsUpdateView.as_view(), name='savings-update'),
    path('income/update/<int:pk>/', UserIncomeUpdateView.as_view(), name='user-income-update'),
    path('income/delete/<int:pk>/', UserIncomeDeleteView.as_view(), name='user-income-delete'),
    path('budget/<int:pk>/update/', BudgetUpdateView.as_view(), name='budget-update'),
    path('budget/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget-delete'),



]
