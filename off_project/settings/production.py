from . import *

SECRET_KEY = ';wsL0*3_k&(M@Vy@.U[!\x0c~AZ'
DEBUG = False
ALLOWED_HOSTS = ['104.236.198.112']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'off', # le nom de notre base de données créée précédemment
        'USER': 'gontrand', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'iutgea',
    }
}
