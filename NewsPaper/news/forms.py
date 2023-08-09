from django.core.mail import send_mail
from django.forms import ModelForm, BooleanField
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'title', 'categories', 'content', 'rating']


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)

        send_mail(
            subject=user.username,
            message='Вы успешно зарегались',
            from_email='ybekberdiyev@yandex.ru',
            recipient_list=[str(user.email), ]
        )

        return user
