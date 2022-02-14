from django.db import models
from django.utils.text import slugify


class Produto(models.Model):
	nome = models.CharField(max_length=255)
	descricao_curta = models.TextField(max_length=255)
	descricao_longa = models.TextField()
	imagem = models.ImageField(
		upload_to='product_images/%Y/%m/', blank=True, null=True)
	slug = models.SlugField(unique=True, blank=True, null=True)
	preco_minimo = models.FloatField()
	preco_maximo = models.FloatField(
        default=0, null=True, blank=True)
	categoria = models.CharField(
		default='',
		max_length=1,
		choices=(
			('C', 'Casacos'),
			('M', 'Moletons'),
			('B', 'Blusas'),
			('A', 'Calças'),
		)
	)

	def __str__(self):
		return self.nome

	
	def save(self, *args, **kwargs):
		if not self.slug:
			slug = f'{slugify(self.nome)}'
			self.slug = slug

		super().save(*args, **kwargs)


class Variacao(models.Model):
	produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
	nome = models.CharField(max_length=50, null=True, blank=True)
	preco = models.FloatField()
	estoque = models.PositiveIntegerField(default=1)


	def __str__(self):
		return self.nome or self.produto.nome


	class Meta:
		verbose_name = 'Variação'
		verbose_name_plural = 'Variações'
