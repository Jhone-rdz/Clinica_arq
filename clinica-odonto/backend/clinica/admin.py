from django.contrib import admin
from .models import Paciente, Prontuario, Consulta, Pagamento, Perfil


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "cpf", "data_nascimento")
    search_fields = ("nome", "cpf")


@admin.register(Prontuario)
class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ("paciente", "data_registro")
    search_fields = ("paciente__nome",)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "dentista", "data_hora", "status")
    list_filter = ("status", "dentista")


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("consulta", "valor", "forma_pagamento", "parcelas", "status")
    list_filter = ("status",)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "perfil")
    list_filter = ("perfil",)
