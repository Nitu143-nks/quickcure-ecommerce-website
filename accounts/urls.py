from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import index  # Assuming your index view is in 'core/views.py'
from accounts import views  # Ensure proper import
from django.contrib.auth.views import LoginView  # Import LoginView here

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # User authentication routes (including the default login page provided by Django)
    path('accounts/', include('django.contrib.auth.urls')),

    # Custom login route with a custom template
    path('accounts/login/', LoginView.as_view(template_name='accounts/logn.html'), name='login'),

    # Registration route
    path('register/', views.register, name='register'),

    # Password reset route
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # Home page route
    path('', index, name='home'),  # Homepage route for index.html

    # Custom login view route (if you want to use a custom login view)
    path('login/', views.login_view, name='login'),

    # Logout route
    path('logout/', views.logout_view, name='logout'),
]
