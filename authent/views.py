from django.shortcuts import render, redirect
from authent.models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

# Create your views here.

def login(request):
    return render(request, 'authn/login.html')


@csrf_exempt
# @login_required
def login_check(request):
    email = request.POST['email']
    password = request.POST['password']
    print("email===>",email)
    print("password===>",password)

    user = authenticate(request, email_address=email, password=password )
    # print(user)
    print("===> user: {}".format(user))
    if user is not None:
        if user.role_fields.role == "Main-Admin":
            print( "user role:",user.role_fields.role)
            # Redirect to Main admin success page.
            auth_login(request, user)
            return redirect(dashboard)
        elif user.role_fields.role == "Sub-Admin":
            # print( "user role:",user.role_fields.role)
            # Redirect to Sub Admin success page.
            print("Sub_Admin")
            auth_login(request, user)
            return redirect(shift_sub_admin)
            # return render(request,"subadmin/base-subadmin.html")
            # return HttpResponse('Sub Admin')
      
    else:
        # Return an 'invalid login' error message.
        messages.error(request, 'username or password not correct')
        return redirect(login)


@login_required
def shift_sub_admin(request):
    return render(request,"subadmin/base-subadmin.html")


@login_required
def dashboard(request):
    return render(request, 'authn/index.html')

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

@login_required
def show_user(request):
    context = dict()
    all_role_data = RoleTable.objects.all()
    context['all_role_data'] = all_role_data
    # print("data===>", all_role_data)
    return render(request, 'authn/user.html', context)

@login_required
def show_user_data(request):
    qry_user = User.objects.all().values(
        'id', 'username', 'email_address', 'role_fields__role'
    )
    return JsonResponse({
        "data": list(qry_user)
    }, safe=False)


@login_required
def show_role(request):
    return render(request, 'authn/role.html')


@login_required
def delete_user(request):
    if request.method == "POST":
        User.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_user)


@login_required
@csrf_exempt
def get_user_ajax(request):
    if request.method == "POST":
        qry_edit_User = User.objects.get(
            id=request.POST['id']
        )
        # print("===>ajax", qry_edit_User)
        return JsonResponse(
            {
                "id": qry_edit_User.id,
                "username": qry_edit_User.username,
                "email_address": qry_edit_User.email_address,
                "password" : qry_edit_User.password,
                "role_fields": qry_edit_User.role_fields.role,
            },
            safe=False
        )


@login_required
@csrf_exempt
def add_user(request):
    User.objects.create(
        username=request.POST['Add_user_name'],
        email_address=request.POST['Add_user_email'],
        password=make_password(request.POST['Add_user_pwd']),

        role_fields=RoleTable.objects.get(id=request.POST['add_role']),
    )

    return redirect(show_user)


@login_required
def edit_user(request):
    User.objects.filter(
        id=request.POST['user_id']
    ).update(
        username=request.POST['edit_user_name'],
        email_address=request.POST['edit_user_email'],
        password=make_password(request.POST['edit_user_pwd']),
        role_fields=request.POST['edit_role'],

    )

    return redirect(show_user)


@login_required
def show_role_data(request):
    qry_role = RoleTable.objects.all().values(
        'id',  'role',  'create_dt', 'is_approve'
    )
    return JsonResponse({
        "data": list(qry_role)
    }, safe=False)


@login_required
@csrf_exempt
def approve_disapprove_role(request):
    """
    :param request: approve_disapprove_id,
                    approve_disapprove_tag
    :return: JsonResponse
    :function: Approve & disapprove Expert Type
    """
    if request.method == 'POST':
        RoleTable.objects.filter(
            id=request.POST['approve_disapprove_id']
        ).update(
            is_approve=request.POST['approve_disapprove_tag'],
        )

        context = {
            'status': True,
            'message': 'Status is update!'
        }
    else:
        context = {
            'status': False,
            'message': 'Get method not allow!'
        }

    return JsonResponse(context)


@login_required
def add_role(request):
    RoleTable.objects.create(
        role=request.POST['Add_role'],

    )

    return redirect(show_role)


@login_required
def delete_role(request):
    """
    :param request: id
    :return: redirect
    :function: delete Weeks
    """
    if request.method == "POST":
        RoleTable.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_role)


@login_required
@csrf_exempt
def get_role_ajax(request):
    if request.method == "POST":
        qry_role = RoleTable.objects.get(
            id=request.POST['id']
        )

        return JsonResponse({
            "id": qry_role.id,
            "role": qry_role.role,
        }, safe=False)


@login_required
def edit_role(request):
    RoleTable.objects.filter(
        id=request.POST['role_id']
    ).update(
        role=request.POST['edit_role'],

    )

    return redirect(show_role)


@login_required
def home(request):
   return render(request,"authn/base.html")


@login_required
def show_devicetype(request):
   return render(request,"authn/devicetype.html")


@login_required
def show_location(request):
   return render(request,"authn/location.html")


@login_required
def show_device_type_data(request):
    qry_device_type = DeviceType.objects.all().values(
        'id',  'device_type',  'create_dt', 'updated_dt', 'is_approve'
    )
    return JsonResponse({
        "data": list(qry_device_type)
    }, safe=False)


@login_required
def add_device_type(request):
   """
    :param request: id
    :return: redirect
    :function: add device type 
   """
   DeviceType.objects.create(
        device_type=request.POST['Add_device_type'],

    )

   return redirect(show_devicetype)


@login_required
@csrf_exempt
def get_device_type_ajax(request):
    if request.method == "POST":
        qry_device_type = DeviceType.objects.get(
            id=request.POST['id']
        )

        return JsonResponse({
            "id": qry_device_type.id,
            "device_type": qry_device_type.device_type,
        }, safe=False)


@login_required
def edit_device_type(request):
   """
    :param request: id
    :return: redirect
    :function: update devive type 
   """
   DeviceType.objects.filter(
        id=request.POST['device_id']
    ).update(
        device_type=request.POST['edit_device_type'],

    )

   return redirect(show_devicetype)


@login_required
def delete_device_type(request):
    """
    :param request: id
    :return: redirect
    :function: delete 
    """
    if request.method == "POST":
        DeviceType.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_devicetype)


@login_required
def show_location_data(request):
    qry_location = Location.objects.all().values(
        'id',  'location', 'create_dt', 'updated_dt', 'is_approve'
    )
    return JsonResponse({
        "data": list(qry_location)
    }, safe=False)


@login_required
def add_Location(request):
    Location.objects.create(
        location=request.POST['add_Location_data'],

    )

    return redirect(show_location)


@login_required
@csrf_exempt
def get_location_ajax(request):
    if request.method == "POST":
        qry_location = Location.objects.get(
            id=request.POST['id']
        )

        return JsonResponse({
            "id": qry_location.id,
            "location": qry_location.location,
        }, safe=False)


@login_required
def edit_location(request):
    """
    :param request: id
    :return: redirect
    :function: edit location
    """
    Location.objects.filter(
        id=request.POST['location_id']
    ).update(
        location=request.POST['edit_location_data'],

    )

    return redirect(show_location)


@login_required
def delete_location(request):
    """
    :param request: id
    :return: redirect
    :function: delete location
    """
    if request.method == "POST":
        Location.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_location)


@login_required
def show_Department(request):
    return render(request, "authn/department.html")


@login_required
def show_department_data(request):
    qry_department_name = Department.objects.all().values(
        'id',  'department_name',  'create_dt', 'updated_dt'
    )
    return JsonResponse({
        "data": list(qry_department_name)
    }, safe=False)


@login_required
def add_department_data(request):
   """
    :param request: id
    :return: redirect
    :function: add device type 
   """
   Department.objects.create(
        department_name=request.POST['add_department_name'],

    )

   return redirect(show_Department)


@login_required
@csrf_exempt
def get_department_name_ajax(request):
    if request.method == "POST":
        qry_department_name = Department.objects.get(
            id=request.POST['id']
        )

        return JsonResponse({
            "id": qry_department_name.id,
            "department_name": qry_department_name.department_name,
        }, safe=False)


@login_required
def edit_department_name(request):
    """
    :param request: id
    :return: redirect
    :function: edit location
    """
    Department.objects.filter(
        id=request.POST['department_name_id']
    ).update(
        department_name=request.POST['edit_department_name'],

    )

    return redirect(show_Department)


@login_required
def delete_department_name(request):
    """
    :param request: id
    :return: redirect
    :function: delete location
    """
    if request.method == "POST":
        Department.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_Department)


@login_required
def show_employees(request):
    context = dict()
    all_emp_data = Department.objects.all()
    context['all_emp_data'] = all_emp_data
    print("data===>", all_emp_data)
    return render(request, "authn/employeesdata.html", context)


@login_required
def show_employees_data(request):
    qry_department_name = EmployeesData.objects.all().values(
        'id',  'Emp_ID',  'emp_name',  'emp_email',  'department_fk__department_name',
        'designation_name',  'manager',  'create_dt', 'updated_dt'
    )
    return JsonResponse({
        "data": list(qry_department_name)
    }, safe=False)


@login_required
def edit_EmployeesData(request):
    EmployeesData.objects.filter(
        id=request.POST['empdata_id']
    ).update(
        Emp_ID=request.POST['edit_Emp_ID'],
        emp_email=request.POST['edit_emp_email'],
        emp_name=request.POST['edit_emp_name'],
        designation_name=request.POST['edit_designation_name'],
        manager=request.POST['edit_manager'],
        # password=make_password(request.POST['edit_user_pwd']),
        department_fk=request.POST['edit_department_fk'],

    )

    return redirect(show_employees)


@login_required
def delete_EmployeesData_type(request):
    """
    :param request: id
    :return: redirect
    :function: delete location
    """
    if request.method == "POST":
        EmployeesData.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_employees)
    

@login_required
def add_emp_data(request):
   """
    :param request: id
    :return: redirect
    :function: add device type 
   """
   EmployeesData.objects.create(
        Emp_ID = request.POST['add_Emp_ID'],
        emp_name = request.POST['add_emp_name'],
        emp_email = request.POST['add_emp_email'],
        # department_fk = request.POST['add_department_fk'],

        department_fk=Department.objects.get(id=request.POST['add_department_fk']),

        designation_name = request.POST['add_designation_name'],
        manager = request.POST['add_manager'],

    )

   return redirect(show_employees)


@login_required
@csrf_exempt
def get_view_fun_EmployeesData_ajax(request):
    if request.method == "POST":
        qry_device = EmployeesData.objects.get(
            id=request.POST['id']
        )

        return JsonResponse({
            "id": qry_device.id,
            "Emp_ID": qry_device.Emp_ID,
            "emp_name": qry_device.emp_name,
            "emp_email": qry_device.emp_email,
            "department_fk": qry_device.department_fk.department_name,
            "designation_name": qry_device.designation_name,
            "manager": qry_device.manager,
            # "memory": qry_device.memory,
            # "location_name": qry_device.location_name.location,
            # "assignee": qry_device.assignee,
            # "additional_comment": qry_device.additional_comment,

            # "create_dt": qry_device.device_type_name__device_type,
            # "updated_dt": qry_device.device_type_name__device_type,
            # "create_by": qry_device.device_type_name__device_type,
            # "is_approve": qry_device.device_type_name__device_type,
        }, safe=False)


@login_required
@csrf_exempt
def get_EmployeesData_ajax(request):
    if request.method == "POST":
        qry_EmployeesData = EmployeesData.objects.get(
            id=request.POST['id']
        )
        # print("===>ajax", qry_edit_User)
        return JsonResponse(
            {
                "id": qry_EmployeesData.id,
                "Emp_ID": qry_EmployeesData.Emp_ID,
                "emp_name": qry_EmployeesData.emp_name,
                "emp_email" : qry_EmployeesData.emp_email,
                "department_fk": qry_EmployeesData.department_fk.department_name,
                "designation_name": qry_EmployeesData.designation_name,
                "manager": qry_EmployeesData.manager,
            },
            safe=False
        )


@login_required
def show_devices(request):
    context = dict()
    all_device_type = DeviceType.objects.all()
    all_location = Location.objects.values()
    context = {'all_device_type': all_device_type,
                'all_location'  : all_location
    }
    # print(context)
    return render(request, "authn/devices.html", context)


@login_required
def show_devices_data(request):
    qry_devices = Device.objects.all().values(
        'id', 'assignee', 'device_type_name__device_type', 'service_tag', 'brand', 'model_no',
        'model_name', 'ram', 'memory', 'location_name__location', 'additional_comment', 'create_dt', 'updated_dt',
        'is_approve'
    )
    return JsonResponse({
        "data": list(qry_devices)
    }, safe=False)


@login_required
@csrf_exempt
def get_view_fun_devices_ajax(request):
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
def add_devices(request):
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

    return redirect(show_devices)


@login_required
@csrf_exempt
def get_devices_ajax(request):
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
        additional_comment = request.POST['edit_device_additional_comments'],###

    )
    return redirect(show_devices)


@login_required
def delete_devices(request):
    """
    :param request: id
    :return: redirect
    :function: delete location
    """
    if request.method == "POST":
        Device.objects.filter(id=request.POST['delete_id']).delete()

    return redirect(show_devices)
