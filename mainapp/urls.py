from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('projects/', project_page, name='projects'),
    path('project/<int:pk>/', project_detail, name='project-detail'),
    path('services/', services_page, name='services'),
    path('chat/<int:id>/', chat_page, name='chat'),
    path('chat-with-freelancer/<str:username>/',
         chat_with_freelancer, name='chat-with-freelancer'),
    # path('services/<int:service_id>/', service_page, name='service'),
    path('freelancers/', freelancers_page, name='freelancers'),
    path('my-orders/<str:status>/', my_orders_page, name='my-orders'),
    path('my-orders-freelancer/<str:status>/',
         my_orders_page_freelancer, name='my-orders-freelancer'),
    path('my-orders-freelancer-detail/<int:order_id>/',
         my_order_active_detail, name='my-orders-freelancer-detail'),
    path('my-orders-completed/<int:order_id>/',
         my_order_completed, name='my-orders-completed'),
    path('my-orders-canceled/<int:order_id>/',
         my_order_canceled, name='my-orders-canceled'),
    path('accounts/profile/user-<int:id>', profile, name='profile'),
    path('create-order/', create_order_page, name='create-order'),
    path('wallet/', wallet_page, name='wallet'),
    path('payment-first-step/', payment_first_step, name='payment-first-step'),
    path('payment-second-step/payment-<int:payment_id>/',
         payment_second_step, name='payment-second-step'),


    path('error/', error_page, name='error'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
