from django.contrib import admin
from .models import MinecraftServer

@admin.register(MinecraftServer)
class MinecraftServerAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "port", "software", "version")
    list_filter = ("status", "software", "version")
    search_fields = ("name", "owner__username")
    readonly_fields = ("created_at", "pid", "server_id")

    fieldsets = (
        (None, {
            "fields": ("name", "owner", "description")
        }),
        ("Server configuration", {
            "fields": ("version", "software", "jar_path", "server_dir_location", "port")
        }),
        ("Resources & Status", {
            "fields": ("allocated_memory", "allocated_cpu_threads", "status", "pid")
        }),
        ("Other", {
            "fields": ("server_id", "created_at")
        })
    )

