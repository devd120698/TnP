from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
admin.site.register(Student)

class BookResource(resources.ModelResource):

    class Meta:
        model = CompanyApplicants
        

class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_filter = ('company','placementStatus')
    list_display= ['student','company','placementStatus','getstudentadmissionNumber','grades']

admin.site.register(Application)
admin.site.register(Resume)
admin.site.register(CompanyApplicants,BookAdmin)