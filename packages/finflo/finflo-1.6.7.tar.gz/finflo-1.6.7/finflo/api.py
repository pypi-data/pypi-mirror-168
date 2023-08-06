from .models import Action, SignList
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .transition import FinFlotransition
from rest_framework.generics import ListAPIView , ListCreateAPIView 
from django.conf import settings
from .serializer import  (
    TransitionManagerserializer,
    Actionseriaizer,
    workflowitemslistserializer,
    workeventslistserializer,
    Workitemserializer
)
from .models import Action , TransitionManager , workevents , workflowitems
from django.db.models import Q



####################################################
################      API       ####################
####################################################



# 1 . TRANSITION MAKING API


class TransitionApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        type = request.data.get("type")
        action = request.data.get("action")
        t_id = request.data.get("t_id")
        if type and action  is not None:
            transitions = FinFlotransition(action = action , type = type , t_id = t_id , state = None )
            return Response({"status" : "Transition success"},status = status.HTTP_200_OK)
        return Response({"status" : "Transition failure"},status = status.HTTP_204_NO_CONTENT)


    


#  2 . ALL WORK_MODEL LIST 


class DetailsListApiView(ListAPIView):
    queryset = TransitionManager.objects.all()
    serializer_class = TransitionManagerserializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        type = self.request.query_params.get('type',None)
        t_id = self.request.query_params.get('t_id',None)
        if t_id and type is not None :
            queryset = TransitionManager.objects.filter(Q(type__icontains = type ) | Q(t_id = int(t_id)))
        elif type is not None and t_id is None:
            queryset = TransitionManager.objects.filter(type__icontains = type)
        else:
            queryset = TransitionManager.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TransitionManagerserializer(queryset, many=True)
        return Response({"status": "success", "type" : settings.FINFLO['WORK_MODEL'] , "data": serializer.data}, status=status.HTTP_200_OK)



# 3 . WORFLOW API 

class WorkFlowitemsListApi(ListAPIView):
    queryset = workflowitems.objects.all()
    serializer_class = Workitemserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = workflowitems.objects.all()
        serializer = Workitemserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)




# WORKEVENTS API 


class WorkEventsListApi(ListAPIView):
    queryset = workevents.objects.all()
    serializer_class = workeventslistserializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = workevents.objects.all()
        serializer = workeventslistserializer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)



# ACTION CREATE AND LIST API 

from django.apps import apps

class ActionListApi(ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = Actionseriaizer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Action.objects.all()
        work_model = settings.FINFLO['WORK_MODEL']  
        for iter in work_model:
            gets_model =  apps.get_model(iter)
            print(gets_model)
            try:
                datas  = gets_model.objects.filter(id = 1).values()
                print(datas)
            except:
                continue
        serializer = Actionseriaizer(queryset, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = Actionseriaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "failure", "data": serializer.errors},status=status.HTTP_204_NO_CONTENT)





