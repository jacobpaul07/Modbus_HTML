from django.shortcuts import render
from typing import List
import json

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.relations import ManyRelatedField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from app.ModbusTCP_MongoDB import modbus_tcp
from .models import employees
from .serializers import employeesSeerializer
from django.http import JsonResponse


class SensorListAPI(APIView):

    def get(self, request):
        sensordatalist = modbus_tcp()
        data = {"data": sensordatalist}
        json_data = json.dumps(data, default=lambda o: o.__dict__, indent=4)
        return HttpResponse(json_data, content_type="application/json")

    def post(self):
        pass

    # @api_view(['GET'])
    # def read_setting( self,request):
    #     filePath = './Json_Class/JSONCONFIG.json'
    #     with open(filePath) as f:
    #         json_string = json.load(request)
    #         json_return = json.dumps(json_string)
    #         f.close()
    #     return HttpResponse(json_return, content_type="application/json")
    #
    # @api_view(['POST'])
    # def write_setting(self, request):
    #     filePath = './Json_Class/JSONCONFIG.json'
    #     with open(filePath, "a") as file:
    #         file.write(json.dumps(request, indent=2))


