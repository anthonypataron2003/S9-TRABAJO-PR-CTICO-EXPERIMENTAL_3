from django.db import migrations, models


def copiar_estado_completado(apps, schema_editor):
    Tarea = apps.get_model("tareas", "Tarea")
    Tarea.objects.filter(completada=True).update(estado="completed")


def restaurar_completada(apps, schema_editor):
    Tarea = apps.get_model("tareas", "Tarea")
    Tarea.objects.filter(estado="completed").update(completada=True)


class Migration(migrations.Migration):

    dependencies = [
        ("tareas", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tarea",
            name="estado",
            field=models.CharField(
                choices=[
                    ("pending", "Pendiente"),
                    ("in_progress", "En proceso"),
                    ("completed", "Completada"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.RunPython(copiar_estado_completado, restaurar_completada),
        migrations.RemoveField(
            model_name="tarea",
            name="completada",
        ),
    ]
