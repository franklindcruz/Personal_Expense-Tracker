from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
<<<<<<< HEAD
    path('admin_site_view/', admin.site.urls),
    path('', include('tracker.urls'))
=======
    path("site-admin-view/", admin.site.urls),
    path("", include("tracker.urls")),
>>>>>>> c0f086d044d9248b1a8ec1983d54145414b86e15
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
