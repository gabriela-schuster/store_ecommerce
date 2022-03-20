from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
import re


class Perfil(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	idade = models.PositiveIntegerField()
	cpf = models.CharField(max_length=11, help_text="Apenas números")
	cidade = models.CharField(max_length=30)
	bairro = models.CharField(max_length=30)
	endereco = models.CharField(max_length=50)
	numero = models.CharField(max_length=5)
	complemento = models.CharField(max_length=30)
	cep = models.CharField(max_length=8)
	estado = models.CharField(
		max_length = 2,
		default ='RS',
		choices = (
			('AC', 'Acre'),
			('AL', 'Alagoas'),
			('AP', 'Amapá'),
			('AM', 'Amazonas'),
			('BA', 'Bahia'),
			('CE', 'Ceará'),
			('DF', 'Distrito Federal'),
			('ES', 'Espírito Santo'),
			('GO', 'Goiás'),
			('MA', 'Maranhão'),
			('MT', 'Mato Grosso'),
			('MS', 'Mato Grosso do Sul'),
			('MG', 'Minas Gerais'),
			('PA', 'Pará'),
			('PB', 'Paraíba'),
			('PR', 'Paraná'),
			('PE', 'Pernambuco'),
			('PI', 'Piauí'),
			('RJ', 'Rio de Janeiro'),
			('RN', 'Rio Grande do Norte'),
			('RS', 'Rio Grande do Sul'),
			('RO', 'Rondônia'),
			('RR', 'Roraima'),
			('SC', 'Santa Catarina'),
			('SP', 'São Paulo'),
			('SE', 'Sergipe'),
			('TO', 'Tocantins'),
		)
	)


	def __str__(self):
		return f'{self.user} - {self.user.first_name} {self.user.last_name}'


	def clean(self):
		error_messages = {}

		if not validate_cpf(self.cpf):
			error_messages['cpf'] = 'Digite um CPF válido (apenas números)'

		if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
			error_messages['cep'] = 'CEP inválido, digite apenas os 8 números do CEP'

		if error_messages:
			raise ValidationError(error_messages)


def validate_cpf(cpf):
	cpf = str(cpf)
	cpf = re.sub(r'[^0-9]', '', cpf)

	if not cpf or len(cpf) != 11:
		return False

	new_cpf = cpf[:-2]
	reverse = 10
	total = 0

	# Loop do CPF
	for index in range(19):
		if index > 8:                   # first index go from 0 to 9
			index -= 9                  # 9 first digits

		total += int(new_cpf[index]) * reverse  # multiplication value

		reverse -= 1
		if reverse < 2:
			reverse = 11
			d = 11 - (total % 11)

			if d > 9:
				d = 0
			total = 0
			new_cpf += str(d)          # Concatena o digito gerado no novo cpf

	# Evita sequencies. Ex.: 11111111111, 00000000000...
	sequency = new_cpf == str(new_cpf[0]) * len(cpf)

	if cpf == new_cpf and not sequency:
		return True
	else:
		return False