from django import forms
from control_panel.models import MinecraftServer

class MinecraftServerForm(forms.ModelForm):
    class Meta:
        model = MinecraftServer
        fields = [
            "name", "description", "port", "allocated_memory", "allocated_cpu_threads",
            "server_dir_location", "software", "version"
        ]