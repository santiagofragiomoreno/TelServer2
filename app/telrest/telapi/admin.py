from django.contrib import admin
from telapi.models import Task, Instruction, Grant, Ownership


class InstructionAdmin(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ['id', 'get_username', 'get_task_name', 'issued_date', 'recieved_date', 'recieved']

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = 'user'  # Allows column order sorting
    get_username.short_description = 'User'  # Renames column head

    def get_task_name(self, obj):
        return obj.task.name

    get_task_name.admin_order_field = 'task'  # Allows column order sorting
    get_task_name.short_description = 'Task'  # Renames column head


admin.site.register(Grant)
admin.site.register(Ownership)
admin.site.register(Task)
admin.site.register(Instruction, InstructionAdmin)
