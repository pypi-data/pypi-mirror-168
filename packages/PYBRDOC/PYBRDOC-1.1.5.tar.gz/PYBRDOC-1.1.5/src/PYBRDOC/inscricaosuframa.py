# -*- coding: utf-8 -*-

import re

from itertools import chain
from random import choice, randint

from .documentoidentificacao import DocumentoIdentificacao

class InscricaoSuframa(DocumentoIdentificacao):
	"""
	Número de inscrição na Superintendência da Zona Franca de Manaus (SUFRAMA)
	"""

	def __init__(self, arg): 
		super(InscricaoSuframa, self).__init__(arg)

	def __str__(self):
		"""
		Formatará uma string de CPF somente com números formatada adequadamente, adicionando visual de formatação padrão
		símbolos de ajuda para exibição.
		Se CPF for Nenhum, retorna uma string vazia; caso contrário, se a string CPF for encurtada para 11 dígitos ou
		contém caracteres sem dígitos, retorna o valor bruto que representa a instância do CPF inválido
		string não formatada.
		"""
		if self.rawValue == None: return str()

		x = self.rawValue

		if not x.isdigit() or len(x) != 9 or len(set(x)) == 1:
			return self.rawValue

		return '{}.{}.{}'.format(x[:2], x[2:6], x[6:])

	@property
	def isValid(self):
		"""
		Retorna se os dígitos de checksum de verificação do `cpf` fornecido correspondem ou não ao seu número base.
		A entrada deve ser uma string de dígitos de comprimento adequado.
		"""
		return ValidadorSuframa.validar(self)



class ValidadorSuframa(object):
	"""
	docstring for ValidadorSuframa
	"""

	def __call__(self, value):
		return ValidadorSuframa.validar(value)


	def __validarInscricaoSuframa(self, arg): # type: (InscricaoSuframa) -> bool
		return self.__validarStr(arg.rawValue)


	def __validarStr(self, arg): # type: (str) -> bool
		if arg == None:
			return False

		p = re.compile('[^0-9]')
		x = p.sub('', arg)

		if len(x) != 9 or len(set(x)) == 1: return False

		p = re.compile('[0126][012].?\\d{4}.?[013][10]\\d')

		if not p.match(x): return False

		return all(self.__hashDigit(x, i + 9) == int(v) for i, v in enumerate(x[8:]))


	def __hashDigit(self, num, position): # type: (str, int) -> int
		"""
		Calculará o dígito de soma de verificação `position` fornecido para a entrada `cpf`. A entrada deve conter todos
		elementos anteriores a `position` senão a computação produzirá o resultado errado.
		"""

		val = sum(int(digit) * weight for digit, weight in zip(num, range(position, 1, -1))) % 11

		return 0 if val < 2 else 11 - val


	@staticmethod
	def validar(arg):

		v = ValidadorSuframa()

		if type(arg) == InscricaoSuframa: return v.__validarInscricaoSuframa(arg)

		if type(arg) == str: return v.__validarStr(arg)

		return False



validar_inscricao_suframa = ValidadorSuframa()



class GeradorSuframa(object):
	"""
	docstring for GeradorSuframa
	"""

	def __hashDigit(self, num, position): # type: (str, int) -> int
		"""
		Calculará o dígito de soma de verificação `position` fornecido para a entrada `cpf`. A entrada deve conter todos
		elementos anteriores a `position` senão a computação produzirá o resultado errado.
		"""

		val = sum(int(digit) * weight for digit, weight in zip(num, range(position, 1, -1))) % 11

		return 0 if val < 2 else 11 - val


	def __checksum(self, baseNum): # type: (str) -> str
		"""
		Calculará os dígitos da soma de verificação para um determinado número de base do CPF. `basenum` precisa ser uma string de dígitos
		de comprimento adequado.
		"""
		return str(self.__hashDigit(baseNum, 9))


	@staticmethod
	def gerar(): # type: () -> InscricaoSuframa
		"""
		Gera aleatoriamente uma inscrição SUFRAMA válida, para fins de testes de softwares em desenvolvimento
		"""

		base = choice(['01','02','10','11','20','60'])
		seq = str(randint(1, 9998)).zfill(4)

		while len(set(seq)) == 1:
			seq = str(randint(1, 9998)).zfill(4) #preencha uma string numérica com zeros à esquerda para preencher um campo da largura fornecida

		base += seq
		base += choice(['01','10','30'])

		g = GeradorSuframa()

		return InscricaoSuframa(base + g.__checksum(base))



