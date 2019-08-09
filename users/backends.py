from .models import User


class EmailBackend(object):
    """
    自定义邮箱登录后台
    """

    @staticmethod
    def authenticate(request, **credentials):
        # 要注意登录表单中用户输入的用户名或者邮箱的 field 名均为 username
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    @staticmethod
    def get_user(user_id):
        """
        该方法是必须的
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
