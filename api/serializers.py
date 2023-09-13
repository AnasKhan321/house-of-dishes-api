from .models import *
from users.models import ChefUser
from rest_framework import serializers

class DishInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishInstruction
        fields = "__all__"

class DishSerializer(serializers.ModelSerializer):
    # instructions = DishInstructionSerializer(many=True, read_only=True)
    class Meta:
        model = Dish
        fields = (
            'name', 'instructions', 'chef', 'veg_non_veg', 'popularity_state',
            'cuisine', 'main_course_starter_dessert', 'quantity', 'customizable_ingredients',
            'cooking_time', 'dish_picture'
        )   
    # def create(self, validated_data):
    #     instructions_data = validated_data.pop('instructions', []) 
    #     dish = Dish.objects.create(**validated_data)
    #     for instruction_data in instructions_data:
    #         DishInstruction.objects.create(**instruction_data)
    #     dish.instruction = DishInstruction
    #     dish.save()
    #     return dish

class DishMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id','name']

class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChefUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']

class ChefListSerializer(serializers.ModelSerializer):
    dishes = serializers.SerializerMethodField()
    class Meta:
        model = ChefUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture', 'dishes']
    def get_dishes(self, obj):
        dishes = Dish.objects.filter(chef=obj)
        return DishMinimalSerializer(dishes, many=True).data
    