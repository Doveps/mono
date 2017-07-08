DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'doveps', 
        'USER': 'postgres', 
        'PASSWORD': 'postgres', 
        'HOST': 'localhost', # the missing piece of the puzzle 
        'PORT': '5432', # optional, I don't need this since I'm using the standard port
    } 
}