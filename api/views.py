from .models import *
from .serializers import *
from .permissions import *
from decouple import config
from users.models import ChefUser
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication


class ChefListView(generics.ListAPIView):
    queryset = ChefUser.objects.all()
    serializer_class = ChefSerializer


class ChefDishesListView(generics.RetrieveAPIView):
    queryset = ChefUser
    serializer_class = ChefListSerializer
    lookup_field = 'pk'


class DishListView(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class DishListCreateView(generics.CreateAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsChef]


class DishUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated, IsChef]


class ContactView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            subject = f"Contact from {name}"
            email_message = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'
            recipients = config('RECIPIENTS').split(',')
            try:
                send_mail(subject, email_message, email, recipients)
                return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Failed to send message.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DishListState(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, state_slug):
        # Query the data to Retrive the Specific Data
        data_queryset = Dish.objects.filter(popularity_state=state_slug)

        # Converting  the QuerySet to a list
        data_list = list(data_queryset)

        # Serializing the data only if it's valid
        serializer = DishSerializer(data=data_list, many=True)
        if serializer.is_valid():
            return Response({'success': True, 'data': serializer.data})
        else:
            # Handle the case where the serializer is not valid (e.g., validation errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishListCourse(APIView):
    permission_classes = []

    def get(self, request, course_slug):

        try:

            # Query the data to Retrive the Specific Data
            data_queryset = Dish.objects.filter(main_course_starter_dessert=course_slug)

            # Converting  the QuerySet to a list
            data_list = list(data_queryset)

            # Serializing the data only if it's valid
            serializer = DishSerializer(data=data_list, many=True)
            if serializer.is_valid():
                return Response({'success': True, 'data': serializer.data })
            else:
                # Handle the case where the serializer is not valid (e.g., validation errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as j:
            return Response({'success ': False, 'error': j})



class DishChoice(APIView):

    permission_classes = []

    def get(self, request, choice_slug):

        try:

            # Query the data to Retrive the Specific Data
            data_queryset = Dish.objects.filter(veg_non_veg=choice_slug)

            # Converting  the QuerySet to a list
            data_list = list(data_queryset)

            # Serializing the data only if it's valid
            serializer = DishSerializer(data=data_list, many=True)
            if serializer.is_valid():
                return Response({'success': True, 'data': serializer.data })
            else:
                # Handle the case where the serializer is not valid (e.g., validation errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_message = str(e)  # Get the string representation of the exception

            return Response({'success': False, 'error': error_message})



class DishById(APIView):
    permission_classes = []

    def get(self, request, dish_id):

        try:

            # Query the data to Retrive the Specific Data
            data_queryset = Dish.objects.filter(id=dish_id)

            # Converting  the QuerySet to a list
            data_list = list(data_queryset)

            # Serializing the data only if it's valid
            serializer = DishSerializer(data=data_list, many=True)
            if serializer.is_valid():
                return Response({'success': True, 'data': serializer.data , 'id' : dish_id})
            else:
                # Handle the case where the serializer is not valid (e.g., validation errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            error_message = str(e)  # Get the string representation of the exception

            return Response({'success': False, 'error': error_message})

class DishByIngredients(APIView):
    permission_classes = []
    serializer_class = DishSerializer

    def post(self, request):
        try:
            filters = request.data
            ingredients = filters['ingredients']

            dishes = Dish.objects.all()
            for ingredient in ingredients:
                dishes = dishes.filter(ingredients__name=ingredient)

            if 'main_course_starter_dessert' in filters:
                dishes = dishes.filter(main_course_starter_dessert=filters['main_course_starter_dessert'])

            if 'veg_non_veg' in filters:
                dishes = dishes.filter(veg_non_veg=filters['veg_non_veg'])

            serializer = DishSerializer(dishes, many=True)

            return Response(serializer.data)
        except Exception as error :
            return  Response({"error" : error})


class DishFilter(APIView):
    permission_classes = []
    serializer_class = DishSerializer

    def post(self, request):
        try:
            filters = request.data
            dishes = Dish.objects.filter(name=filters['name'] , veg_non_veg=filters['veg_non_veg'] , main_course_starter_dessert=filters['course_choice'])
            serializer = DishSerializer(dishes, many=True)
            return  Response({"success" : True , "data" : serializer.data})
        except Exception as j:
            return  Response({"success" : False , "error" : j})