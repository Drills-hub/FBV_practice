from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializers import UserSerializer, Profilerializer
from .models import User


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
@csrf_exempt
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
        token = get_object_or_404(OutstandingToken, token=refresh_token)
        BlacklistedToken.objects.create(token=token)

    return Response({"detail": "로그아웃 성공"}, status=205)


# 토큰 갱신
@api_view(["POST"])
def token_refresh(request):

    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=200)
    else:
        return Response(serializer.errors, status=400)


# 회원탈퇴
@api_view(["DELETE"])
def user_delete(request):
    if request.user.is_authenticated:
        request.user.soft_delete()
        return Response({"detail": "회원탈퇴 성공"}, status=200)
    else:
        return Response({"detail": "잘못된 접근"}, status=404)


# 회원정보 조회
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_profile(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    if request.user != user:
        return Response(
            {"message": "유저정보는 본인의 것만 확인할 수 있습니다"}, status=401
        )

    serializer = Profilerializer(user)
    return Response(serializer.data, status=200)


# 회원정보 수정
@api_view(["PUT"])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_update(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    if request.user != user:
        return Response(
            {"message": "유저정보는 본인의 것만 수정 할 수 있습니다"}, status=401
        )

    serializer = Profilerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=200)


# 비밀번호 수정
@api_view(["POST"])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_password(request):
    user = get_object_or_404(User, username=request.user.username, is_active=True)
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not user.check_password(old_password):
        return Response({"message": "기존 비밀번호가 일치하지 않습니다."}, status=400)

    if old_password == new_password:
        return Response({"message": "기존 비밀번호와 같은 비밀번호입니다."}, status=400)

    request.user.set_password(new_password)
    request.user.save()
    return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=200)
