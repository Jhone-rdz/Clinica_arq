from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.timezone import make_aware

from .models import Consulta, Paciente, Pagamento, Prontuario


# ---------------- AUTENTICAÇÃO -----------------


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("password")
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(
                request,
                "clinica/login.html",
                {"erro": "Usuário ou senha inválidos."},
            )

    return render(request, "clinica/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- DASHBOARD -----------------


@login_required
def dashboard(request):
    total_pacientes = Paciente.objects.count()
    consultas_hoje = Consulta.objects.filter(status="agendado").count()
    pendentes = Pagamento.objects.filter(status="pendente").count()

    ctx = {
        "total_pacientes": total_pacientes,
        "consultas_hoje": consultas_hoje,
        "pendentes": pendentes,
    }
    return render(request, "clinica/dashboard.html", ctx)


# ---------------- PACIENTES -----------------


@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, "clinica/pacientes_list.html", {"pacientes": pacientes})


@login_required
def novo_paciente(request):
    if request.method == "POST":
        Paciente.objects.create(
            nome=request.POST["nome"],
            telefone=request.POST["telefone"],
            endereco=request.POST["endereco"],
            data_nascimento=request.POST["data_nascimento"],
            cpf=request.POST["cpf"],
        )
        return redirect("lista_pacientes")

    return render(request, "clinica/paciente_form.html")


# ---------------- PRONTUÁRIO -----------------


@login_required
def ver_prontuario(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    prontuarios = Prontuario.objects.filter(paciente=paciente).order_by("-data_registro")
    ctx = {
        "paciente": paciente,
        "prontuarios": prontuarios,
    }
    return render(request, "clinica/prontuario.html", ctx)


@login_required
def novo_prontuario(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    if request.method == "POST":
        Prontuario.objects.create(
            paciente=paciente,
            historico=request.POST.get("historico", ""),
            evolucao=request.POST.get("evolucao", ""),
            alergias=request.POST.get("alergias", ""),
            observacoes=request.POST.get("observacoes", ""),
            imagem=request.FILES.get("imagem"),
        )
        return redirect("ver_prontuario", paciente_id=paciente.id)

    return render(request, "clinica/prontuario_form.html", {"paciente": paciente})


# ---------------- AGENDA -----------------


@login_required
def lista_consultas(request):
    consultas = Consulta.objects.all().order_by("data_hora")
    return render(request, "clinica/agenda.html", {"consultas": consultas})


@login_required
def nova_consulta(request):
    if request.method == "POST":
        paciente_id = request.POST["paciente"]
        dentista_id = request.POST["dentista"]
        data_hora_str = request.POST["data_hora"]  # formato: 2025-11-25T14:00

        # converte string do input datetime-local
        dt = datetime.fromisoformat(data_hora_str)
        dt_aware = make_aware(dt)

        consulta = Consulta.objects.create(
            paciente_id=paciente_id,
            dentista_id=dentista_id,
            data_hora=dt_aware,
        )

        # opcional: criar um pagamento "pendente" automático
        Pagamento.objects.create(
            consulta=consulta,
            valor=request.POST.get("valor", 0) or 0,
            forma_pagamento=request.POST.get("forma_pagamento", "A definir"),
            parcelas=int(request.POST.get("parcelas", 1) or 1),
        )

        return redirect("agenda")

    ctx = {
        "pacientes": Paciente.objects.all(),
        "dentistas": User.objects.all(),
    }
    return render(request, "clinica/consulta_form.html", ctx)


# ---------------- FINANCEIRO -----------------


@login_required
def financeiro(request):
    pagamentos = Pagamento.objects.all()
    total_recebido = sum(
        p.valor for p in pagamentos if p.status == "pago"
    )
    total_pendente = sum(
        p.valor for p in pagamentos if p.status == "pendente"
    )

    ctx = {
        "pagamentos": pagamentos,
        "total_recebido": total_recebido,
        "total_pendente": total_pendente,
    }
    return render(request, "clinica/financeiro.html", ctx)


# ---------------- RELATÓRIOS -----------------


@login_required
def relatorios(request):
    total_pacientes = Paciente.objects.count()
    total_consultas = Consulta.objects.count()
    atendimentos_concluidos = Consulta.objects.filter(status="concluido").count()
    faturamento = sum(
        p.valor for p in Pagamento.objects.filter(status="pago")
    )
    pendentes = Pagamento.objects.filter(status="pendente").count()

    ctx = {
        "total_pacientes": total_pacientes,
        "total_consultas": total_consultas,
        "atendimentos_concluidos": atendimentos_concluidos,
        "faturamento": faturamento,
        "pendentes": pendentes,
    }
    return render(request, "clinica/relatorios.html", ctx)
