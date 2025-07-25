from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("sys_dashboard",views.sys_dashboard, name="sys_dashboard"),
    path("show_devices_sys",views.show_devices_sys, name="show_devices_sys"),
    path("show_devices_record",views.show_devices_record, name="show_devices_record"),
    path("show_devices_record_data",views.show_devices_record_data, name="show_devices_record_data"),
    path("add_devices_sys",views.add_devices_sys, name="add_devices_sys"),
    path("edit_devices_sys",views.edit_devices_sys, name="edit_devices_sys"),
    path("edit_devices_sys",views.edit_devices_sys, name="edit_devices_sys"),
    path("delete_devices_sys",views.delete_devices_sys, name="delete_devices_sys"),
    path("show_devices_data_sys",views.show_devices_data_sys, name="show_devices_data_sys"),
    path("get_view_fun_devices_ajax_sys",views.get_view_fun_devices_ajax_sys, name="get_view_fun_devices_ajax_sys"),
    path("get_devices_ajax_sys",views.get_devices_ajax_sys, name="get_devices_ajax_sys"),
   
] 