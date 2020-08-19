from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from django.db.models import fields

# Register your models here.

class BookResource1(resources.ModelResource):
	student_name = Field(attribute='student__name',column_name='student_name')
	cgpa = Field(attribute='student__CGPA',column_name='cgpa')
	branch = Field(attribute='student__branch',column_name='branch')
	student = Field(column_name='Roll_no')
	# st_name = fields.CharField('student__name', null=True)
	class Meta:
		model = CompanyApplicants
		fields = ['id','student_name','student','company','placementStatus']
		export_order = ('id', 'student_name','student','company', 'cgpa','branch')
		exclude = ('placementStatus', )

class BookResource2(resources.ModelResource):
	
	class Meta:
		model = Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('admissionNumber', 'rollNumber')
    list_display_links = ('admissionNumber', 'rollNumber')
		

class BookAdmin1(ImportExportModelAdmin):
	resource_class = BookResource1
	list_filter = ('company','placementStatus')
	list_display= ['student','company','placementStatus']


class BookAdmin2(ImportExportModelAdmin):
	resource_class = BookResource2
	list_filter = ('branch','CGPA')
	list_display= ['name','admissionNumber','branch','CGPA']




admin.site.register(Student,BookAdmin2)
admin.site.register(Application)
admin.site.register(Resume)
admin.site.register(CompanyApplicants,BookAdmin1)