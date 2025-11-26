from django.urls import path
from . import views

urlpatterns = [
    # autenticação
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # dashboard
    path("", views.dashboard, name="dashboard"),

    # pacientes
    path("pacientes/", views.lista_pacientes, name="lista_pacientes"),
    path("pacientes/novo/", views.novo_paciente, name="novo_paciente"),

    # prontuário
    path("prontuario/<int:paciente_id>/", views.ver_prontuario, name="ver_prontuario"),
    path(
        "prontuario/<int:paciente_id>/novo/",
        views.novo_prontuario,
        name="novo_prontuario",
    ),

    # agenda
    path("agenda/", views.lista_consultas, name="agenda"),
    path("agenda/nova/", views.nova_consulta, name="nova_consulta"),

    # financeiro
    path("financeiro/", views.financeiro, name="financeiro"),

    # relatórios
    path("relatorios/", views.relatorios, name="relatorios"),
]
