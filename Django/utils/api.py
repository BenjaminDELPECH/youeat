from django.conf import settings


def getDjangoApiUrl():
    url = settings.API_URL +'/graphql/'
    return url