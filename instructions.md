### Instructions 

## Go to setting > bottom and  put your mail and Password:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'Trial@gmail.com'
EMAIL_HOST_PASSWORD = '**** **** **** ****'
```

## Replace App name in Installed app
```
INSTALLED_APPS = [
    ...

    "Home", #replace it with your Home app name
    "SysAuth"
]
```

## Home > `urls.py` 

Change URL for your apps

## AuthSys > templates > AuthSys > 'contain all html templates'

## change App_name in `urls.py` for link refrence

```
{% url 'App_name:login' %}
```

## Install
```
pip install celery redis
```