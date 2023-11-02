from .models import *
from users.models import ChefUser
from rest_framework import serializers


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructions
        fields = ('step','instruction_video_url')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity')


class DishSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    instructions = InstructionSerializer(many=True)

    class Meta:
        model = Dish
        fields = (
            'name', 'ingredients', 'instructions', 'chef', 'veg_non_veg', 'popularity_state',
            'cuisine', 'main_course_starter_dessert',
            'cooking_time', 'dish_picture',
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instructions_data = validated_data.pop('instructions')
        dish = Dish.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(dish=dish, **ingredient_data)
        for instruction_data in instructions_data:
            Instructions.objects.create(dish=dish, **instruction_data)
        return dish


class DishMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name']


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