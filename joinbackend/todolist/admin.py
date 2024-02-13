from django.contrib import admin
from .models import TodoItem,Contacts,TaskAssignments,SubtasksList,Subtask

# class TodoAdmin(admin.ModelAdmin):    
#     fields = ('title','date','description','category' ,'color','prio','state','checked','assignments')  
#     list_display = ('title','date','description','category' ,'color','prio','state','checked','assignments')    
#     search_fields = ('title',)
    
    
class ContactAdmin(admin.ModelAdmin):    
    fields = ( 'email' , 'name', 'iconColor' , 'phone', 'short','user')    
    list_display = ('email' , 'name', 'iconColor' , 'phone', 'short','user')    
    search_fields = ('name',)
    
# class ContactAdmin(admin.ModelAdmin):    
#     fields = ( 'email' , 'name', 'password')    
#     list_display = ('email' , 'name', 'iconColor' , 'phone', 'short')    
#     #search_fields = ('text',) 

# # Register your models here.
#admin.site.register(TodoItem,TodoAdmin)
admin.site.register(Contacts,ContactAdmin)

@admin.register(TodoItem)
class TodoAdmin(admin.ModelAdmin): 
     fields = ('title','date','description','category' ,'color','prio','state','checked')  
     list_display = ('title','date','description','category' ,'color','prio','state','checked')    
     search_fields = ('title',)
     
@admin.register(TaskAssignments)
class TaskAssignmentsAdmin(admin.ModelAdmin): 
     fields = ('todoitem','contact')  
     list_display = ('todoitem','contact') 
     
@admin.register(SubtasksList)
class SubtasksListAdmin(admin.ModelAdmin): 
     fields = ('todoitem','subtask')  
     list_display = ('todoitem','subtask')    
        
@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin): 
     fields = ('checked','title')  
     list_display = ('checked','title')       