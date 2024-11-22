from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
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


# 로그인 구현
@api_view(["POST"])
def login_session(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response(
            {"message": "로그인 성공"}, status=200
        )
    return Response({"error": "잘못된 로그인 정보"}, status=401)


# 로그아웃 구현
@api_view(["POST"])
def logout_session(request):
    if request.user.is_authenticated:
        logout(request)
    return Response({"message": "로그아웃 성공"}, status=200)
