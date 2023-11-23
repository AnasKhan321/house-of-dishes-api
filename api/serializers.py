from .models import *
from users.models import ChefUser
from rest_framework import serializers


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructions
        fields = ('id','step', 'instruction_video_url' , 'time')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity' , 'unit')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name',)



class DishSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)
    courses = CourseSerializer(many=True)

    class Meta:
        model = Dish
        fields = (
            'id', 'name','created_at','updated_at', 'ingredients', 'instructions', 'chef', 'veg_non_veg', 'popularity_state',
            'cuisine',  'kitchen_equipments' ,'cooking_time', 'dish_picture', 'description' , 'courses'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instructions_data = validated_data.pop('instructions')
        courses_data = validated_data.pop('courses')
        dish = Dish.objects.create(**validated_data)
        for course in courses_data:
            Course.objects.create(dish=dish, **course)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(dish=dish, **ingredient_data)
        for instruction_data in instructions_data:
            Instructions.objects.create(dish=dish, **instruction_data)
        return dish


class DishMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'created_at','updated_at','cuisine', 'courses']


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']


class ChefListSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()

    class Meta:
        model = ChefUser
        fields = ['id', 'first_name', 'last_name',
                  'email', 'profile_picture', 'dishes']

    def get_dishes(self, obj):
        dishes = Dish.objects.filter(chef=obj)
        return DishMinimalSerializer(dishes, many=True).data


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()
