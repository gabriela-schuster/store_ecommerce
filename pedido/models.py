from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	total = models.FloatField()
	status = models.CharField(
		default="C",
		max_length=1,
		choices = (
			('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
		)
	)

	def __str__(self):
		return f'pedido N. {self.pk}'


class ItemPedido(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
	produto_nome = models.CharField(max_length=255)
	produto_id = models.PositiveIntegerField()
	variacao = models.CharField(max_length=255)
	variacao_id = models.PositiveIntegerField
	preco = models.FloatField()
	quantidade = models.PositiveIntegerField
	imagem = models.CharField(max_length=2000)

	def __str__(self):
		return f'item {self.produto_nome} do {self.pedido}'

	class Meta:
		verbose_name = 'Item do pedido'
		verbose_name_plural = 'Itens do pedido'
