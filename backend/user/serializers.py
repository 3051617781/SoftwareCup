from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User

# 自定义邮箱重复注册错误信息
class CustomUniqueValidator(UniqueValidator):
    def __call__(self, value, serializer_field):
        self.message = '邮箱 %s 已经存在' % value
        return super().__call__(value, serializer_field)


class CustomUserCreateSerializer(UserCreateSerializer):
    # 进行邮箱唯一验证
    email = serializers.EmailField(
        validators = [CustomUniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        