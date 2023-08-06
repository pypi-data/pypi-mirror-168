django-front-door
===================


Simple, easy to use, middleware to lock access to any django app based on request attributes.

Quick Start
===========

Add `FrontDoorMiddleware` to your `settings.MIDDLEWARE` as first as possible.

    MIDDLEWARE = (
         'front_door.middleware.FrontDoorMiddleware',
         'django.contrib.sessions.middleware.SessionMiddleware',
         'django.middleware.common.CommonMiddleware',
         'django.middleware.csrf.CsrfViewMiddleware',
         'django.contrib.auth.middleware.AuthenticationMiddleware',
         'django.contrib.messages.middleware.MessageMiddleware',
    )

Configure 
