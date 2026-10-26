from django.db import models


class Tarea(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pending", "Pendiente"
        EN_PROCESO = "in_progress", "En proceso"
        COMPLETADA = "completed", "Completada"

    titulo = models.CharField(max_length=120)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]

    def __str__(self):
        return self.titulo
