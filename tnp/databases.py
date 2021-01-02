DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'NAME': 'tnp',
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'turbodrive',
    },
    'wsdc_student': {
        'NAME': 'wsdc_student',
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'turbodrive',
    },
    'coordinators': {
        'NAME': 'coordinators',
        'HOST': '127.0.0.1',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'turbodrive',
    }
}