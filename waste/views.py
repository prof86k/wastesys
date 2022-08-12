from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpRequest

# Create your views here.
def add_place_to_cover(request: HttpRequest,*args, **kwargs) -> JsonResponse:
    '''Add places to cover for waste collection'''
    if request.is_ajax():
        return JsonResponse()

def add_waste_type_collected(request: HttpRequest, *args, **kwargs) -> JsonResponse:
    if request.is_ajax():
        return JsonResponse()
