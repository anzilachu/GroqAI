# from django.urls import path

# from .views import chat_completion_william

# urlpatterns = [
#     path('', chat_completion_william, name='chat_completion_william'),
# ]

from django.urls import path

from .views import chat_completion_author,home,search_author, create_author, register, login_user,custom_logout

urlpatterns = [
    path('', home, name='home'),
    path('chat/<str:author_name>/', chat_completion_author, name='chat_completion_author'),
    path('search/', search_author, name='search_author'),
    path('create_author/', create_author, name='create_author'),

    path('register/',register, name='register'),  # URL for registration view
    path('login/', login_user, name='login'), 
    path('logout/', custom_logout, name='logout'),
]