from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from .serializers import UserSerializer


# 회원가입
@api_view(["POST"])
def signup(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# 세션 로그인 구현
@api_view(["POST"])
def login_session(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"message": "로그인 성공"}, status=200)
    return Response({"error": "잘못된 로그인 정보"}, status=401)


# 세션 로그아웃 구현
@api_view(["POST"])
def logout_session(request):
    if request.user.is_authenticated:
        logout(request)
    return Response({"message": "로그아웃 성공"}, status=200)


# jwt 로그인 구현
@api_view(["POST"])
def login_jwt(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    refresh = RefreshToken.for_user(user)

    if user is not None:
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=200,
        )

    return Response({"error": "잘못된 로그인 정보"}, status=401)


# jwt 로그아웃 구현
@api_view(["POST"])
def logout_jwt(request):

    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return Response({"message": "리프레시 토큰이 필요합니다"}, status=400)

    else:
        token = OutstandingToken.objects.get(token=refresh_token)
        BlacklistedToken.objects.create(token=token)

    return Response({"detail": "로그아웃 성공"}, status=205)
