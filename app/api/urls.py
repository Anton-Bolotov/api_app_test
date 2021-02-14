from django.urls import path
from config import config
from .views import *

param = config()

urlpatterns = [
    path(f'{param["endpoint"]}/{param["version"]}/user/<int:user_id>/comment/<int:message_id>/', user_message_info),
    path(f'{param["endpoint"]}/{param["version"]}/user/<int:user_id>/comment/', all_user_message),
    path(f'{param["endpoint"]}/{param["version"]}/user/<int:user_id>/', user_info),
    path(f'{param["endpoint"]}/{param["version"]}/comment/<int:message_id>/', comment_info),
]
