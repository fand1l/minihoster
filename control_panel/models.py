from django.db import models
from django.contrib.auth.models import User

class MinecraftServer(models.Model):
    class SoftwareChoices(models.TextChoices):
        VANILLA = "vanilla", "Vanilla"
        PAPER = "paper", "Paper"
        FOLIA = "folia", "Folia"
        VELOCITY = "velocity", "Velocity"
        ARCLIGHTE = "arclight", "Arclight"
        FABRIC = "fabric", "Fabric"
        FORGE = "forge", "Forge"
        NEOFORGE = "neoforge", "NeoForge"
        QUILT = "quilt", "Quilt"

    class StatusChoices(models.TextChoices):
        RUNNING = "running", "Running"
        STOPPED = "stopped", "Stopped"
        SLEEPING = "sleeping", "Sleeping"

    server_id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)

    jar_path = models.CharField(max_length=500)
    allocated_memory = models.IntegerField(default=4096)
    allocated_cpu_threads = models.IntegerField(default=2)
    server_dir_location = models.CharField(max_length=500)

    port = models.IntegerField(unique=True)
    status = models.CharField(
        choices=StatusChoices.choices,
        max_length=10,
        default=StatusChoices.STOPPED)
    pid = models.IntegerField(null=True, blank=True)

    software = models.CharField(
        choices=SoftwareChoices.choices,
        max_length=20)
    version = models.CharField(
        default="latest",
        max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.owner.username})"