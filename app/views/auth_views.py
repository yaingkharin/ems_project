from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# DTO-named serializers
from app.dto.requests.user_request import CreateUserRequest
from app.dto.responses.user_response import UserResponse
from app.dto.requests.auth_request import LoginRequestDTO
from app.dto.responses.auth_response import LoginResponseDTO
from app.services.user_service import UserService
from app.services.authentication_service import AuthenticationService
from app.utils.jwt import JWTUtil
from app.utils.api_response import api_response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user.",
        request_body=CreateUserRequest,
        responses={
            201: UserResponse,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            user_response_dto = UserService.create_user(validated_data)

            return api_response(
                data=user_response_dto,
                message="User created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Authenticate user and get JWT tokens.",
        request_body=LoginRequestDTO,
        responses={
            200: LoginResponseDTO,
            400: "Bad Request",
            401: "Unauthorized"
        }
    )
    def post(self, request):
        serializer = LoginRequestDTO(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data.get('email')
        password = validated_data.get('password')

        user_response_dto = UserService.authenticate_user(email, password)

        if user_response_dto:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user_instance = User.objects.get(id=user_response_dto['id'])
                tokens = JWTUtil.generate_tokens(user_instance)

                response_data = {
                    "accessToken": tokens['access_token'],
                    "refreshToken": tokens['refresh_token']
                }
                return api_response(
                    data=response_data,
                    message="Login successful.",
                    status_code=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return api_response(
                    message="User not found after authentication.",
                    success=False,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return api_response(
                message="Invalid credentials.",
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout user (requires authentication).",
        responses={
            200: "Successfully logged out."
        }
    )
    def post(self, request):
        return api_response(
            message="Successfully logged out.",
            status_code=status.HTTP_200_OK
        )

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login or Register via Google OAuth.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_token': openapi.Schema(type=openapi.TYPE_STRING, description='Google ID Token')
            },
            required=['id_token']
        ),
        responses={
            200: "Login Successful",
            401: "Authentication Failed"
        }
    )
    def post(self, request):
        id_token = request.data.get('id_token')
        if not id_token:
            return api_response(
                message="Google id_token is required.",
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            auth_data = AuthenticationService.google_login(id_token)
            return api_response(
                data=auth_data,
                message="Google login successful.",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return api_response(
                message=str(e),
                success=False,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
