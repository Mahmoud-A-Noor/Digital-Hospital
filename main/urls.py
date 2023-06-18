"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .consumer import NotificationConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('account/', include('accounts.urls')),
    path('model/', include('ai.urls')),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('pharmacist/', include('pharmacist.urls')),
    path('manager/', include('system_admin.urls')),
    
    path('about-us/', about_us, name="about-us"),
    path('contact-us/', contact_us, name="contact-us"),
    path('brain_tumor_info/', brain_tumor_info, name="brain_tumor_info"),
]

websocket_urlpatterns = [
    path('ws/doctor/<int:user_id>/', NotificationConsumer.as_asgi()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .consumer import NotificationConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('account/', include('accounts.urls')),
    path('model/', include('ai.urls')),
    path('patient/', include('patient.urls')),
    path('doctor/', include('doctor.urls')),
    path('pharmacist/', include('pharmacist.urls')),
    path('manager/', include('system_admin.urls')),
    
    path('about-us/', about_us, name="about-us"),
    path('contact-us/', contact_us, name="contact-us"),
    path('pneumonia_info/', pneumonia_info, name="pneumonia_info"),
    path('brain_tumor_info/', brain_tumor_info, name="brain_tumor_info"),
    path('diabetic_retinopathy_info/', diabetic_retinopathy_info, name="diabetic_retinopathy_info"),

    path('mark_user_notifications_as_read/', mark_user_notifications_as_read, name="mark_user_notifications_as_read"),
]

websocket_urlpatterns = [
    path('ws/doctor/<int:user_id>/', NotificationConsumer.as_asgi()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)