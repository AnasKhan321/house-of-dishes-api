from .models import *
from .serializers import *
from django.views import View
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta

class RedirectSocial(View):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        return JsonResponse(json_obj)


class ChefListCreateView(generics.ListCreateAPIView):
    queryset = ChefUser.objects.all()
    serializer_class = ChefAccountSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ChefAccountSerializer(data=request.data)
        if serializer.is_valid():
            chef = serializer.save()
            refresh = RefreshToken.for_user(chef)
            refresh.access_token.set_exp(lifetime=timedelta(hours=3))
            access = str(refresh.access_token)
            data = {
                "account_id": chef.id,
                "email": chef.email,
                "first_name": chef.first_name,
                "access_token": access,
                "refresh_token": str(refresh)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class ChefRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChefUser.objects.all()
    serializer_class = ChefAccountSerializer

    def get_object(self):
        return self.request.user


class ChefLoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = ChefLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            refresh.access_token.set_exp(lifetime=timedelta(hours=3))
            access_token = str(refresh.access_token)
            data = {
                "account_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "access_token": access_token,
                "refresh_token": str(refresh)
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({"message": "Unable to login with given credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pass
        pass


class GraphicListCreateView(generics.ListCreateAPIView):
    queryset = GraphicUser.objects.all()
    serializer_class = GraphicUserSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = GraphicUserSerializer(data=request.data)
        if serializer.is_valid():
            Graphic = serializer.save()
            refresh = RefreshToken.for_user(Graphic)
            access = str(refresh.access_token)
            refresh.access_token.set_exp(lifetime=timedelta(hours=3))
            data = {
                "account_id": Graphic.id,
                "email": Graphic.email,
                "first_name": Graphic.first_name,
                "access_token": access,
                "refresh_token": str(refresh)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class GraphicLoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = GraphicLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh.access_token.set_exp(lifetime=timedelta(hours=3))
            data = {
                "account_id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "access_token": access_token,
                "refresh_token": str(refresh)
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response({"message": "Unable to login with given credentials."}, status=status.HTTP_401_UNAUTHORIZED)

def send_email(email):
    subject = f'Your account email verification'
    message = f'To login into ai chef master dashboard follow this link http://dashboard.aichefmaster.com//login/{email}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])

class VerifyEmail(APIView):
    permission_classes = []
    def post(self, request):
        try:
            if 'email' in request.data:
                Email = request.data['email']
                send_email(Email)
                return Response({'success': True, 'message': f"Log in Url is Successfull send to the Email  : {Email}"})
            else:
                return Response({'success': False, 'message': "Email is Required "})

        except Exception as error:
            return Response({'success': False, 'message': error})
