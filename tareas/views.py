from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Tarea


def lista(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        if titulo:
            Tarea.objects.create(titulo=titulo)
        return redirect("lista")
    tareas = Tarea.objects.all()
    completadas = Tarea.objects.filter(estado=Tarea.Estado.COMPLETADA).count()
    en_proceso = Tarea.objects.filter(estado=Tarea.Estado.EN_PROCESO).count()
    pendientes = Tarea.objects.filter(estado=Tarea.Estado.PENDIENTE).count()
    total_tareas = tareas.count()
    return render(
        request,
        "tareas/lista.html",
        {
            "tareas": tareas,
            "total_tareas": total_tareas,
            "completadas": completadas,
            "pendientes": pendientes,
            "en_proceso": en_proceso,
            "progreso": round(completadas * 100 / total_tareas) if total_tareas else 0,
            "porcentaje_pendientes": round(pendientes * 100 / total_tareas) if total_tareas else 0,
            "porcentaje_en_proceso": round(en_proceso * 100 / total_tareas) if total_tareas else 0,
            "ultimas_tareas": tareas[:3],
            "tareas_pendientes": tareas.filter(estado=Tarea.Estado.PENDIENTE)[:3],
            "tareas_en_proceso": tareas.filter(estado=Tarea.Estado.EN_PROCESO)[:3],
            "tareas_completadas": tareas.filter(estado=Tarea.Estado.COMPLETADA)[:3],
            "tareas_de_hoy": tareas.filter(creada__date=timezone.localdate()).count(),
        },
    )


def editar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    error = ""

    if request.method == "POST":
        titulo = request.POST.get("titulo", "").strip()
        if titulo:
            tarea.titulo = titulo
            tarea.save(update_fields=["titulo"])
            return redirect("lista")
        error = "Escribe un título para la tarea."

    return render(
        request,
        "tareas/editar.html",
        {"tarea": tarea, "error": error},
    )


@require_POST
def completar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    siguiente_estado = request.POST.get("estado")
    estados_validos = {estado for estado, _ in Tarea.Estado.choices}
    if siguiente_estado is not None and siguiente_estado not in estados_validos:
        return HttpResponseBadRequest("Estado de tarea no válido.")
    if siguiente_estado is not None:
        tarea.estado = siguiente_estado
    elif tarea.estado == Tarea.Estado.COMPLETADA:
        tarea.estado = Tarea.Estado.PENDIENTE
    else:
        tarea.estado = Tarea.Estado.COMPLETADA
    tarea.save(update_fields=["estado"])
    return redirect("lista")


@require_POST
def eliminar(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.delete()
    return redirect("lista")


def salud(request):
    return JsonResponse({"status": "ok"})
