from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Tarea
class TareaModelTest(TestCase):
    def test_str_devuelve_titulo(self):
        tarea = Tarea.objects.create(titulo="Estudiar CI/CD")
        self.assertEqual(str(tarea), "Estudiar CI/CD")
    def test_estado_pendiente_por_defecto(self):
        tarea = Tarea.objects.create(titulo="Practicar Docker")
        self.assertEqual(tarea.estado, Tarea.Estado.PENDIENTE)
class TareaViewsTest(TestCase):
    def test_lista_responde_200(self):
        respuesta = self.client.get(reverse("lista"))
        self.assertEqual(respuesta.status_code, 200)

    def test_menu_espacio_trabajo_muestra_secciones(self):
        respuesta = self.client.get(reverse("lista"))
        self.assertContains(respuesta, "Mis tareas")
        self.assertContains(respuesta, "En proceso")
        self.assertContains(respuesta, "Completadas")
        self.assertContains(respuesta, "Progreso")
    def test_crear_tarea(self):
        self.client.post(reverse("lista"), {"titulo": "Nueva tarea"})
        self.assertEqual(Tarea.objects.count(), 1)
    def test_lista_muestra_resumen_de_tareas(self):
        Tarea.objects.create(titulo="Pendiente")
        Tarea.objects.create(titulo="En proceso", estado=Tarea.Estado.EN_PROCESO)
        Tarea.objects.create(titulo="Terminada", estado=Tarea.Estado.COMPLETADA)
        respuesta = self.client.get(reverse("lista"))
        self.assertEqual(respuesta.context["total_tareas"], 3)
        self.assertEqual(respuesta.context["pendientes"], 1)
        self.assertEqual(respuesta.context["completadas"], 1)
        self.assertEqual(respuesta.context["en_proceso"], 1)
        self.assertEqual(respuesta.context["progreso"], 33)
        self.assertEqual(respuesta.context["tareas_pendientes"].count(), 1)
        self.assertEqual(respuesta.context["tareas_completadas"].count(), 1)
        self.assertEqual(respuesta.context["tareas_en_proceso"].count(), 1)

    def test_lista_vacia_muestra_progreso_cero(self):
        respuesta = self.client.get(reverse("lista"))

        self.assertEqual(respuesta.context["progreso"], 0)

    def test_lista_cuenta_tareas_creadas_hoy(self):
        Tarea.objects.create(titulo="Tarea de hoy")
        tarea_anterior = Tarea.objects.create(titulo="Tarea anterior")
        Tarea.objects.filter(pk=tarea_anterior.pk).update(
            creada=timezone.now() - timedelta(days=3)
        )

        respuesta = self.client.get(reverse("lista"))

        self.assertEqual(respuesta.context["tareas_de_hoy"], 1)
        self.assertContains(respuesta, "Pendientes por iniciar")
        self.assertContains(respuesta, "En proceso")
        self.assertContains(respuesta, "Últimas completadas")
        self.assertContains(respuesta, "Tu actividad de hoy")
        self.assertContains(respuesta, "Estadísticas del espacio")
        self.assertContains(respuesta, "Accesos rápidos")

    def test_editar_tarea(self):
        tarea = Tarea.objects.create(titulo="Título original")

        respuesta = self.client.post(
            reverse("editar", args=[tarea.pk]),
            {"titulo": "Título actualizado"},
        )

        tarea.refresh_from_db()
        self.assertEqual(tarea.titulo, "Título actualizado")
        self.assertRedirects(respuesta, reverse("lista"))

    def test_editar_tarea_rechaza_titulo_vacio(self):
        tarea = Tarea.objects.create(titulo="Título original")

        respuesta = self.client.post(
            reverse("editar", args=[tarea.pk]),
            {"titulo": "   "},
        )

        tarea.refresh_from_db()
        self.assertEqual(tarea.titulo, "Título original")
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Escribe un título para la tarea.")

    def test_completar_tarea_requiere_post(self):
        tarea = Tarea.objects.create(titulo="Hacer deber")
        respuesta = self.client.get(reverse("completar", args=[tarea.pk]))

        tarea.refresh_from_db()
        self.assertEqual(respuesta.status_code, 405)
        self.assertEqual(tarea.estado, Tarea.Estado.PENDIENTE)

    def test_completar_tarea(self):
        tarea = Tarea.objects.create(titulo="Hacer deber")
        respuesta = self.client.post(reverse("completar", args=[tarea.pk]))

        tarea.refresh_from_db()
        self.assertEqual(tarea.estado, Tarea.Estado.COMPLETADA)
        self.assertRedirects(respuesta, reverse("lista"))

    def test_cambiar_estado_a_en_proceso(self):
        tarea = Tarea.objects.create(titulo="Iniciar tarea")

        respuesta = self.client.post(
            reverse("completar", args=[tarea.pk]),
            {"estado": Tarea.Estado.EN_PROCESO},
        )

        tarea.refresh_from_db()
        self.assertEqual(tarea.estado, Tarea.Estado.EN_PROCESO)
        self.assertRedirects(respuesta, reverse("lista"))

    def test_cambiar_estado_rechaza_estado_no_valido(self):
        tarea = Tarea.objects.create(titulo="Tarea pendiente")

        respuesta = self.client.post(
            reverse("completar", args=[tarea.pk]),
            {"estado": "desconocido"},
        )

        tarea.refresh_from_db()
        self.assertEqual(respuesta.status_code, 400)
        self.assertEqual(tarea.estado, Tarea.Estado.PENDIENTE)

    def test_eliminar_tarea(self):
        tarea = Tarea.objects.create(titulo="Eliminar")

        respuesta = self.client.post(reverse("eliminar", args=[tarea.pk]))

        self.assertFalse(Tarea.objects.filter(pk=tarea.pk).exists())
        self.assertRedirects(respuesta, reverse("lista"))

    def test_endpoint_salud(self):
        respuesta = self.client.get(reverse("salud"))
        self.assertEqual(respuesta.json(), {"status": "ok"})
