"""
URL configuration for SkillSwap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.generic import TemplateView
from profiles.views import dashboard_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Static pages
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('features/', TemplateView.as_view(template_name="features.html"), name="features"),
    path('how-it-works/', TemplateView.as_view(template_name="how-it-works.html"), name="how"),

    # Apps
    path('users/', include('users.urls')),
    # path('profile/', include('profiles.urls')),
    path('matching/', include('matching.urls')),
    path('swap/', include('swap.urls')),
    path('profile/', include('profiles.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("chat/", include("chat.urls")),
    path("calls/", include("calls.urls")),
    path("resources/", include("resources.urls")),


] 

# Media files hamesha serve karo (DEBUG=True ya False dono mein) —
# warna production mein (Railway) uploaded images/attachments 404 denge.
# Chhote projects ke liye ye theek hai; bade scale pe S3/Cloudinary use karna behtar hai.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)