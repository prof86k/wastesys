import email
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse,HttpRequest
from django.contrib import messages as msg

from . import models as mdl
from accounts import models as acmdl
from . import forms as fms
# Create your views here.
def is_ajax(request):
    '''return valid for ajax call'''
    return request.META.get("HTTP_X_REQUESTED_WITH") == 'XMLHttpRequest'

def edit_waste_places_covered(request: HttpRequest, location_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ Update the content of the requested waste location covered
    '''
    waste_location = get_object_or_404(mdl.WasteLocation,id=location_id)
    if request.method == 'POST':
        form = fms.WasteTypeForm(instance=waste_location,data=request.POST)
        if form.is_valid():
            form.save()
            msg.success(request,'Record Updated Successfully')
            return redirect('waste:add_places')
            # JsonResponse({
                # 'success':{
                    # 'msg':'Record updated successfully'
                # }
            # })
    else:
        form = fms.WasteLocationForm(instance=waste_location)
    context = {
        'form':form,
        'waste_location':waste_location
    }
    return render(request,'waste/edit_places.html',context)

def delete_waste_location_covered(request: HttpRequest,location_id: int ,*args, **kwargs) -> HttpResponse:
    '''
    @ erase the records of the waste type collected
    '''
    waste_location = get_object_or_404(mdl.WasteLocation,id=location_id)
    waste_location.delete()
    msg.success(request,'Record Deleted Successfully')
    return redirect('waste:add_places')

def add_place_to_cover(request: HttpRequest,*args, **kwargs) -> JsonResponse:
    '''
    @ Add places to cover for waste collection
    '''
    places = mdl.WasteLocation.objects.order_by('-date_updated').all()
    if request.method == "POST":
        form = fms.WasteLocationForm(request.POST)
        if form.is_valid():
            form.save()
            msg.success(request,'Record Added Successfully.')
            return redirect('waste:add_places')
            # JsonResponse({
                # 'success':{
                    # 'msg':'Record Added successfully'
                # }
            # })
    else:
        form = fms.WasteLocationForm()
    context = {
        'form':form,
        'places':places,
    }
    return  render(request,'waste/add_places.html',context)

def edit_waste_type_collected(request: HttpRequest, waste_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ Update the content of the requested waste type collected
    '''
    waste_type = get_object_or_404(mdl.WasteType,id=waste_id)
    if request.method == 'POST':
        form = fms.WasteTypeForm(instance=waste_type,data=request.POST)
        if form.is_valid():
            form.save()
            msg.success(request,'Record updated successfully')
            return redirect('waste:add_type')
    else:
        form = fms.WasteTypeForm(instance=waste_type)
    context = {
        'form':form,
        'waste_type':waste_type
    }
    return render(request,'waste/edit_waste.html',context)

def add_waste_type_collected(request: HttpRequest, *args, **kwargs) -> HttpResponse:
    '''
    @ Add the waste type a user can request to dispose form
    @ list the waste type collected
    @ Add the waste type a user can request to dispose
    '''
    waste_types = mdl.WasteType.objects.order_by('-date_updated').all()
    if request.method == 'POST':
        form = fms.WasteTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('waste:add_type')
    else:
        form = fms.WasteTypeForm()
    context = {
        'waste_types':waste_types,
        'form':form,
    }
    return render(request,'waste/add_waste.html',context)

def delete_waste_type_collected(request: HttpRequest,waste_id: int ,*args, **kwargs) -> HttpResponse:
    '''
    @ erase the records of the waste type collected
    '''
    waste_type = get_object_or_404(mdl.WasteType,id=waste_id)
    waste_type.delete()
    msg.success(request,'Record Deleted Successfully')
    return redirect('waste:add_type')


def request_was_disposal(request: HttpRequest,*args, **kwargs) -> HttpResponse:
    '''
    @ send the disposable bins
    @ a user fill in the waste disposal form and submit
    '''
    waste_ready     = mdl.DustBin.objects.order_by('-date_created').filter(bin_ready=True,empty_bin=False).all()
    if request.method == 'POST':
        form = fms.DustBinForm(request.POST)
        if form.is_valid():
            new_waste_bin = form.save(commit=False)
            new_waste_bin.user = request.user
            new_waste_bin.empty_bin = False
            new_waste_bin.save()
            msg.success(request,'Record Added Successfully')
            return redirect('waste:dispose_waste')
    else:
        form = fms.DustBinForm()
    context = {
    'form':form,
    'waste_ready':waste_ready
    }
    return render(request,'waste/request_disposal.html',context)

def view_waste_sent(request: HttpRequest) -> HttpResponse:
    '''
    @ list the disposed bins
    @ list the ready bins
    '''
    waste_collected = mdl.DustBin.objects.order_by('-date_updated').filter(user=request.user).all()

    context = {
        'waste_collected':waste_collected,
    }
    return render(request,'waste/view_wastes.html',context)

def edit_waste_bin(request: HttpRequest,bin_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ update the record of existing waste bin
    '''
    waste_bin = get_object_or_404(mdl.DustBin,id=bin_id)
    if request.method == 'POST':
        form = fms.DustBinForm(instance=waste_bin,data=request.POST)
        if form.is_valid():
            form.save()
            msg.success(request,'Record Updated Successfully')
            return redirect('waste:dispose_waste')
    else:
        form = fms.DustBinForm(instance=waste_bin)
    context = {
        'form':form,
        'waste_bin':waste_bin
    }
    return render(request,'waste/edit_disposed_waste.html',context)

def check_waste_bin(request: HttpRequest,bin_id: int, *args, **kwargs) -> HttpResponse:
    '''
    @ update the record of existing waste bin
    '''
    waste_bin = get_object_or_404(mdl.DustBin,id=bin_id)
    settings = mdl.WasteSettings.objects.filter(location=waste_bin.location,waste_type=waste_bin.waste_type).first()
    if request.method == 'POST':
        form = fms.WastePaymentForm(request.POST)
        if form.is_valid() and not waste_bin.payment_made:
            user    = form.cleaned_data.get('user')
            amount = form.cleaned_data.get('amount')
            mdl.WasteDisposalPayment.objects.create(
                user=acmdl.User.objects.filter(email=user).first(),
                amount= mdl.WasteSettings.objects.filter(dues=amount,location=waste_bin.location,waste_type=waste_bin.waste_type).first(),
                payment_confirmation=True)
            waste_bin.payment_made = True
            waste_bin.save()
            msg.success(request,'Payment made successfully')
            return redirect('waste:check_waste',bin_id=waste_bin.id)
        else:
            msg.info(request,'Payment made already')
            return redirect('waste:check_waste',bin_id=waste_bin.id)
    else:
        form = fms.WastePaymentForm()
    context = {
        'waste_bin':waste_bin,
        'form':form,
        'settings':settings,
    }
    return render(request,'waste/check_waste.html',context) 

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
    waste_settings = mdl.WasteSettings.objects.order_by('-date_created').all()
    if request.method == 'POST':
        form    = fms.WasteSettingsForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('waste:waste_settings')
    else:
        form = fms.WasteSettingsForm()
    context = {
        'form':form,
        'waste_settings':waste_settings,
    }
    return render(request,'waste/waste_settings.html',context)
