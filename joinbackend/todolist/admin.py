from django.contrib import admin
from .models import TodoItem,Contacts

class TodoAdmin(admin.ModelAdmin):    
    fields = ('title','date', 'author', 'assignments')    
    list_display = ('date','title')    
    #search_fields = ('text',)
    
    
class ContactAdmin(admin.ModelAdmin):    
    fields = ( 'email' , 'name', 'iconColor' , 'phone', 'short')    
    list_display = ('email' , 'name', 'iconColor' , 'phone', 'short')    
    #search_fields = ('text',)
    
class ContactAdmin(admin.ModelAdmin):    
    fields = ( 'email' , 'name', 'password')    
    list_display = ('email' , 'name', 'iconColor' , 'phone', 'short')    
    #search_fields = ('text',) 

# Register your models here.
admin.site.register(TodoItem,TodoAdmin)
admin.site.register(Contacts,ContactAdmin)