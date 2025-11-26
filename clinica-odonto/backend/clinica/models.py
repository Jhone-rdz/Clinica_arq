from django.db import models
from django.contrib.auth.models import User


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.nome


class Prontuario(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    historico = models.TextField(blank=True)
    evolucao = models.TextField(blank=True)
    alergias = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)
    imagem = models.ImageField(upload_to="prontuarios/", blank=True, null=True)
    data_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prontuário de {self.paciente.nome} em {self.data_registro}"


class Perfil(models.Model):
    PERFIS = [
        ("admin", "Administrador"),
        ("dentista", "Dentista"),
        ("secretaria", "Secretária"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil = models.CharField(max_length=20, choices=PERFIS)

    def __str__(self):
        return f"{self.user.username} - {self.get_perfil_display()}"


class Consulta(models.Model):
    STATUS = [
        ("agendado", "Agendado"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    dentista = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="agendado")

    def __str__(self):
        return f"{self.paciente.nome} - {self.data_hora} ({self.status})"


class Pagamento(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    forma_pagamento = models.CharField(max_length=50)
    parcelas = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default="pendente")  # pendente | pago
    data_pagamento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Pagamento #{self.id} - {self.consulta.paciente.nome} ({self.status})"
