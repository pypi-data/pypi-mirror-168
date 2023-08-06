
from pickle import FALSE
import re

class DocumentoIdentificacao(object):
	"""docstring for DocumentoIdentificacao"""

	__valor = str()

	def __new__(cls, *args, **kwargs):
		if cls == DocumentoIdentificacao:
			raise Exception('Esta classe não pode ser instanciada diretamente!')
		else:
			#return super(DocumentoIdentificacao, cls).__new__(cls, *args, **kwargs)
			return super().__new__(cls)

	def __init__(self, arg):
		self.__valor = self.__sieve(arg)

	def __repr__(self):
		return "<{0}.{1}({2!r})>".format(self.__class__.__module__, self.__class__.__name__, self.rawValue)

	def __str__(self):
		pass

	@property
	def rawValue(self):
		return self.__valor

	def isValid(self):
		return FALSE

	def __sieve(self, input):
		"""
		Filtra os símbolos de formatação do CNPJ. Os símbolos que não são utilizados na formatação do CNPJ são deixados
		não filtrada propositalmente para que se reprovar em outros testes, pois sua presença indica que o
		entrada estava de alguma forma corrompida.
		"""
		p = re.compile('[ ./-]')

		return p.sub('', str(input)) if input != None else None





