from .views import *
from django.urls import path

urlpatterns = [
    path('dish/', DishListView.as_view(), name='dish_list'),
    path('dish/create/', DishListCreateView.as_view(), name='dish_create'),
    path('dish/<int:pk>/', DishUpdateDeleteView.as_view(), name='dish_update_delete'),
    path('chef/', ChefListView.as_view(), name='chef_list_create'),
    path('chef/<int:pk>/dishes/', ChefDishesListView.as_view(), name='chef_dishes'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('dish/filter/<str:state_slug>/state' , DishListState.as_view() , name='dish_by_state'),
    path('dish/filter/<str:course_slug>/course' ,DishListCourse.as_view() , name="dish_list_course" ),
    path('dish/filter/<str:choice_slug>/choice' ,DishChoice.as_view() , name="dish_list_choice" ),
    path('dish/filter/<int:dish_id>/id' ,DishById.as_view() , name="dish_by_id" ),
    path('dish/filter/<str:dish_name>/name' ,DishByName.as_view() , name="dish_by_name" ),
    path('dish/byIngredients' , DishByIngredients.as_view() ,name="Dish-Ingredients"),
    path('dish/filter/search' , DishFilter.as_view() , name="search-dish")

]
