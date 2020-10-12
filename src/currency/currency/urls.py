from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('rate/', include('rate.urls')),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
