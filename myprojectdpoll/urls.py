from django.contrib import admin
from django.urls import path
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static
from myprojectdpoll import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_voter, name='login_voter'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.ForgetPassword, name='forgot'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('changepassword/<token>/', views.ChangePassword, name='changepassword'),
    path('logout/', views.Logout, name='logout'),
    path('otp/', views.otp, name='otp'),
    path('setpassword/<str:unique_id>/', views.set_password, name='set_password'),
]

# Add static file handling for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)