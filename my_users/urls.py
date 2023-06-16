from .views import register,login

from django.urls import path

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('reg', register.as_view() ),
    path ('login',login.as_view())
]
