from django.contrib import admin
from authent.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(RoleTable)
admin.site.register(DeviceType)
admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(EmployeesData)
admin.site.register(Device)
admin.site.register(Location)