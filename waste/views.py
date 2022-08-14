from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.contrib import messages as msg

from . import models as mdl
from . import forms as fms
# Create your views here.

def places_covered(request:HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ add the places to cover form
    @ list the places covered
    '''
    form = fms.WasteLocationForm()
    places = mdl.WasteLocation.objects.order_by('-date_updated').all()
    context = {
        'form':form,
        'places':places
    }
    return render(request,'',context)

def edit_waste_places_covered(request: HttpRequest, location_id: int, *args, **kwargs) -> JsonResponse:
    '''
    @ Update the content of the requested waste location covered
    '''
    waste_location = get_object_or_404(mdl.WasteLocation,id=location_id)
    if request.is_ajax():
        form = fms.WasteTypeForm(instance=waste_location,data=request.POST)
        if form.is_valid():
            form.save()
            # msg.success(request,)
            return JsonResponse({
                'success':{
                    'msg':'Record updated successfully'
                }
            })
    else:
        form = fms.WasteTypeForm(instance=waste_location)
    context = {
        'form':form,
        'waste_location':waste_location
    }
    return render(request,'',context)

def delete_waste_location_covered(request: HttpRequest,location_id: int ,*args, **kwargs) -> HttpResponse:
    '''
    @ erase the records of the waste type collected
    '''
    waste_location = get_object_or_404(mdl.WasteLocation,id=location_id)
    waste_location.delete()
    msg.success(request,'Record Deleted Successfully')
    return redirect('waste:waste_location')

def add_place_to_cover(request: HttpRequest,*args, **kwargs) -> JsonResponse:
    '''
    @ Add places to cover for waste collection
    '''
    if request.is_ajax():
        form = fms.WasteLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success':{
                    'msg':'Record Added successfully'
                }
            })

def waste_type_collected(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ Add the waste type a user can request to dispose form
    @ list the waste type collected
    '''
    form = fms.WasteTypeForm()
    waste_types = mdl.WasteType.objects.order_by('-date_updated').all()
    context = {
        'form':form,
        'waste_types':waste_types
    }
    return render(request,'',context)

def edit_waste_type_collected(request: HttpRequest, waste_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ Update the content of the requested waste type collected
    '''
    waste_type = get_object_or_404(mdl.WasteType,id=waste_id)
    if request.is_ajax():
        form = fms.WasteTypeForm(instance=waste_type,data=request.POST)
        if form.is_valid():
            form.save()
            # msg.success(request,'Record updated successfully')
            return JsonResponse({
                'success':{
                    'msg':'Record updated successfully',
                }
            })
    else:
        form = fms.WasteTypeForm(instance=waste_type)
    context = {
        'form':form,
        'waste_type':waste_type
    }
    return render(request,'',context)

def add_waste_type_collected(request: HttpRequest, *args, **kwargs) -> JsonResponse:
    '''
    @ Add the waste type a user can request to dispose
    '''
    if request.is_ajax():
        form = fms.WasteTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success':{
                    'msg':'Record Added successfully'
                }
            })

def delete_waste_type_collected(request: HttpRequest,waste_id: int ,*args, **kwargs) -> HttpResponse:
    '''
    @ erase the records of the waste type collected
    '''
    waste_type = get_object_or_404(mdl.WasteType,id=waste_id)
    waste_type.delete()
    msg.success(request,'Record Deleted Successfully')
    return redirect('waste:waste_type')

def waste_disposal(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ send the disposable bins
    @ list the disposed bins
    @ list the ready bins
    '''
    form = fms.DustBinForm()
    waste_collected = mdl.DustBin.objects.filter(empty_bin=True).all()
    waste_ready     = mdl.DustBin.objects.filter(bin_ready=True,empty_bin=False).all()
    context = {
        'form':form,
        'waste_collected':waste_collected,
        'waste_ready':waste_ready
    }
    return render(request,'',context)

def request_was_disposal(request: HttpRequest,*args, **kwargs) -> HttpResponse:
    '''
    @ a user fill in the waste disposal form and submit
    '''
    if request.method == 'POST':
        form = fms.DustBinForm(request.POST)
        if form.is_valid():
            new_waste_bin = form.save(commit=False)
            new_waste_bin.user = request.user
            new_waste_bin.save()
            return redirect('waste:waste_disposed')
    else:
        form = fms.DustBinForm()
    context = {'form':form}
    return render(request,'',context)

def edit_waste_bin(request: HttpRequest,bin_id: int, *args, **kwargs) -> JsonResponse:
    '''
    @ update the record of existing waste bin
    '''
    waste_bin = get_object_or_404(mdl.DustBin,id=bin_id)
    if request.is_ajax():
        form = fms.DustBinForm(instance=waste_bin,data=request.POST)
        if form.is_valid():
            form.save()
            # msg.success(request,'')
            return JsonResponse({
                'success':{
                    'msg':'Record Updated Successfully'
                }
            })
            # redirect('waste:waste_disposed')
    else:
        form = fms.DustBinForm(instance=waste_bin)
    context = {
        'form':form,
        'waste_bin':waste_bin
    }
    return render(request,'',context)

def delete_waste_bin(request: HttpRequest,bin_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ delete any bin that is required
    '''
    dust_bin = get_object_or_404(mdl.DustBin,id=bin_id)
    dust_bin.delete()
    msg.success(request,'Record Deleted successfully')
    return redirect('waste:waste_disposed')

def add_waste_settings(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ add the waste settings for every waste to be disposed
    '''
    waste_settings = mdl.WasteSettings.objects.first()
    if request.method == 'POST':
        form    = fms.WasteSettingsForm(instance=waste_settings, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('waste:settings')
    else:
        form = fms.WasteSettingsForm(instance=waste_settings)
    context = {
        'waste_settings':waste_settings,
    }
    return render(request,'',context)
