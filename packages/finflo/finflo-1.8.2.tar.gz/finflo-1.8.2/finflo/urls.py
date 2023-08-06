from django.urls import path
from .api import (
    TransitionApiView ,
    ActionListApi,
    DetailsListApiView,
    WorkFlowitemsListApi,
    WorkEventsListApi
)


urlpatterns = [
    path('action/',ActionListApi.as_view()),
    path('model/',DetailsListApiView.as_view()),
    path('workflowitems/',WorkFlowitemsListApi.as_view()),
    path('workevents/',WorkEventsListApi.as_view()),
    path('transition/',TransitionApiView.as_view())
]
