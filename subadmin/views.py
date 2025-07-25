from django.shortcuts import render,redirect
from authent.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def sys_dashboard(request):
#    return HttpResponse("hello")
   return render(request,"subadmin/base-subadmin.html")


@login_required
def show_devices_sys(request):
    context = dict()
    all_device_type = DeviceType.objects.all()
    all_location = Location.objects.values()
    context = {'all_device_type': all_device_type,
                'all_location'  : all_location
    }
    print(context)
    return render(request, "subadmin/devices.html", context)
# #    return HttpResponse("hello")
#    return render(request,"subadmin/base-subadmin.html")


login_required
def show_devices_data_sys(request):
    qry_devices = Device.objects.all().values(
        'id', 'assignee', 'device_type_name__device_type', 'service_tag', 'brand', 'model_no',
        'model_name', 'ram', 'memory', 'location_name__location', 'additional_comment', 'create_dt', 'updated_dt',
        'is_approve'
    )
    return JsonResponse({
        "data": list(qry_devices)
    }, safe=False)


@login_required
def add_devices_sys(request):
    Device.objects.create(
        device_type_name=DeviceType.objects.get(id=request.POST['add_device_type']),
      
        assignee = request.POST['add_device_assignee'],
        service_tag = request.POST['add_service_tag'],
        brand =request.POST['add_brand'],
        model_no = request.POST['add_model_no'],
        model_name = request.POST['add_model_name'],
        ram = request.POST['add_ram'],
        memory = request.POST['add_memory'],
        additional_comment = request.POST['add_device_additional_comments'],####

        location_name =Location.objects.get(id=request.POST['add_location']),
        
       
    )

    return redirect(show_devices_sys)


@login_required
@csrf_exempt
def get_view_fun_devices_ajax_sys(request):
    if request.method == "POST":
        qry_device = Device.objects.get(
            id=request.POST['id']
        )

        return JsonResponse({
            "id": qry_device.id,
            "device_type_name": qry_device.device_type_name.device_type,
            "service_tag": qry_device.service_tag,
            "brand": qry_device.brand,
            "model_no": qry_device.model_no,
            "model_name": qry_device.model_name,
            "ram": qry_device.ram,
            "memory": qry_device.memory,
            "location_name": qry_device.location_name.location,
            "assignee": qry_device.assignee,
            "additional_comment": qry_device.additional_comment,

            # "create_dt": qry_device.device_type_name__device_type,
            # "updated_dt": qry_device.device_type_name__device_type,
            # "create_by": qry_device.device_type_name__device_type,
            # "is_approve": qry_device.device_type_name__device_type,
        }, safe=False)

@login_required
def edit_devices_sys(request):
    """
    :param request: id
    :return: redirect
    :function: edit location
    """
    Device.objects.filter(
        id=request.POST['device_id']
    ).update(
        device_type_name=request.POST['edit_device_type_name'],
        service_tag=request.POST['edit_service_tag'],
        brand=request.POST['edit_brand'],
        model_no=request.POST['edit_model_no'],
        model_name=request.POST['edit_model_name'],
        ram=request.POST['edit_ram'],
        memory=request.POST['edit_memory'],
        location_name=request.POST['edit_location'],
        assignee=request.POST['edit_device_assignee'],
        additional_comment = request.POST['edit_device_additional_comments'],###

    )
    return redirect(show_devices_sys)


@login_required
@csrf_exempt
def get_devices_ajax_sys(request):
    if request.method == "POST":
        qry_devices = Device.objects.get(
            id=request.POST['id']
        )
        # print("===>ajax.{}", qry_devices.format)
        return JsonResponse(
            {
                "id": qry_devices.id,
                "device_type_name": qry_devices.device_type_name.device_type,
                "service_tag": qry_devices.service_tag,
                "brand": qry_devices.brand,
                "model_no": qry_devices.model_no,
                "model_name": qry_devices.model_name,
                "ram" : qry_devices.ram,
                "memory" : qry_devices.memory,
                "location_name": qry_devices.location_name.location,
                "assignee": qry_devices.assignee,
                "additional_comment": qry_devices.additional_comment,
            },
            safe=False
        )


@login_required
def edit_devices(request):
    """
    :param request: id
    :return: redirect
    :function: edit location
    """
    Device.objects.filter(
        id=request.POST['device_id']
    ).update(
        device_type_name=request.POST['edit_device_type_name'],
        service_tag=request.POST['edit_service_tag'],
        brand=request.POST['edit_brand'],
        model_no=request.POST['edit_model_no'],
        model_name=request.POST['edit_model_name'],
        ram=request.POST['edit_ram'],
        memory=request.POST['edit_memory'],
        location_name=request.POST['edit_location'],
        assignee=request.POST['edit_device_assignee'],

    )
    return redirect(show_devices_sys)


@login_required
def delete_devices_sys(request):
    """
    :param request: id
    :return: redirect
    :function: delete location
    """
    if request.method == "POST":
        Device.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_devices_sys)


@login_required
def show_devices_record(request):
    return render(request, "subadmin/record.html")


@login_required
def show_devices_record_data(request):
    qry_department_name = Device.objects.all().values(
        'id',  'assignee', 'model_no', 'location_name__location',
        'updated_dt'
    )
    return JsonResponse({
        "data": list(qry_department_name)
    }, safe=False)
