from django.contrib.auth.models import User
from users.models import Profile
import logging
import datetime
from django.conf import settings


def getUserId(context):
    user = context.user
    if not user.is_authenticated:
        return -1
        # user = manageAnonymousUserId(context, user)
    return user.id


def manageAnonymousUserId(context, user):
    ip = get_client_ip(context)
    anonymous_user_id = int(context.COOKIES['anonymousUserId'])
    user_nb_with_user_id = User.objects.filter(id=anonymous_user_id).count()
    if user_nb_with_user_id == 0:
        createAnonymousUser(ip, anonymous_user_id)
    user = User.objects.get(id=anonymous_user_id)
    return user


def createAnonymousUser(ip, new_user_id):
    new_user = User(id=new_user_id, username="anonymous_user" + str(new_user_id))
    profil = Profile(age=35, poid=70, taille=175, activity=1.375, sexe=1, user_id=new_user_id, ip_adress=ip, anonyme_account=True)
    new_user.save()
    profil.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def set_cookie(response, key, value, days_expire=100000):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)
