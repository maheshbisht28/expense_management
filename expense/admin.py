from django.contrib import admin


from .models import  User,Category, Expense

class Usertable(admin.ModelAdmin):
	list_display = ("id","first_name","last_name","email","is_student",
		"is_staff","is_superuser")


class Categorytable(admin.ModelAdmin):
	list_display = ("id","c_name")


class Expensetable(admin.ModelAdmin):
	list_display = ("id","user","category","ex_name","date","money","desc")


# class attendancetable(admin.ModelAdmin):
# 	list_display = ("id","user","subject","status","classtime","actualclasstime")

# class classtimetable(admin.ModelAdmin):
# 	list_display = ("id","course","subject","date")


    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}
  
    #search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}

#admin.site.register(attendance1, Att)
admin.site.register(User,Usertable)
admin.site.register(Category,Categorytable)
admin.site.register(Expense,Expensetable)
