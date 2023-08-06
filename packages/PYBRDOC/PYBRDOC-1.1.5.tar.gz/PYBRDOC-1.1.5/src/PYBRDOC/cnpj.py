
import re
import requests
import json
from itertools import chain
from random import randint

from .documentoidentificacao import DocumentoIdentificacao

class Cnpj(DocumentoIdentificacao):
	"""docstring for Cnpj"""

	def __init__(self, arg): 
		super().__init__(arg)

	def __str__(self):
		"""
		Formatará uma string CNPJ somente de números formatada adequadamente, adicionando visual de formatação padrão
		símbolos de ajuda para exibição.
		Se a string do CNPJ for menor que 14 dígitos ou contiver caracteres que não sejam dígitos, retornará o valor bruto
		Cadeia CNPJ não formatada.
		"""

		if self.rawValue == None: return str()

		x = self.rawValue

		if not x.isdigit() or len(x) != 14 or len(set(x)) == 1: return self.rawValue

		return '{}.{}.{}/{}-{}'.format(x[:2], x[2:5], x[5:8], x[8:12], x[12:])

	@property
	def isValid(self):
		"""
		Retorna se os dígitos de checksum de verificação do `cnpj` fornecido correspondem ou não ao seu número base.
		A entrada deve ser uma string de dígitos de comprimento adequado.
		"""
		return ValidadorCnpj.validar(self)




class ValidadorCnpj(object):
	"""docstring for ValidadorCnpj"""

	def __call__(self, value):
		return ValidadorCnpj.validar(value)

	def __validarCnpj(self, arg): 
		return self.__validarStr(arg.rawValue)

	def __validarStr(self, arg): 
		if arg == None:
			return False

		p = re.compile('[^0-9]')
		x = p.sub('', arg)

		if len(x) != 14 or len(set(x)) == 1: return False

		return all(self.__hashDigit(x, i + 13) == int(v) for i, v in enumerate(x[12:]))


	def __hashDigit(self, cnpj, position): # type: (str, int) -> int
		"""
		Calculará o dígito de soma de verificação `position` fornecido para a entrada `cnpj`. A entrada deve conter
		todos os elementos anteriores a `position` senão a computação produzirá o resultado errado.
		"""

		weighten = chain(range(position - 8, 1, -1), range(9, 1, -1))
		val = sum(int(digit) * weight for digit, weight in zip(cnpj, weighten)) % 11

		return 0 if val < 2 else 11 - val

	@staticmethod
	def validar(arg): 
		v = ValidadorCnpj()

		if type(arg) == Cnpj: return v.__validarCnpj(arg)

		if type(arg) == str: return v.__validarStr(arg)

		return False
	
	def consulta_cnpj(self,cnpj):

		url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"

		querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}

		response = requests.request("GET", url, params=querystring)
		resp=json.loads(response.text)
		print("Nome:",resp['nome'])
		print("Data de abertura:",resp['abertura'])
		print("Empresa:",resp['porte'])
		print("Situação atual:",resp['situacao'])
		print("Faz isso:",resp['atividade_principal'])
		print("Natureza Juridica:",resp['natureza_juridica'])
		print("Onde fica:",resp['municipio'])
		print("Contato:",resp['telefone'])
		
	

validar_cnpj = ValidadorCnpj()

	


class GeradorCnpj(object):

	def __hashdigit(self, cnpj, position):
		"""
		Calculará o dígito de soma de verificação `position` fornecido para a entrada `cnpj`. A entrada deve conter
		todos os elementos anteriores a `position` senão a computação produzirá o resultado errado.
		"""

		weighten = chain(range(position - 8, 1, -1), range(9, 1, -1))
		val = sum(int(digit) * weight for digit, weight in zip(cnpj, weighten)) % 11

		return 0 if val < 2 else 11 - val

	def __checksum(self, basenum):
		"""
		Calculará os dígitos da soma de verificação para um determinado número base do CNPJ. `basenum` precisa ser uma string de dígitos
	de comprimento adequado.
		"""

		digitos = str(self.__hashdigit(basenum, 13))
		digitos += str(self.__hashdigit(basenum + digitos, 14))

		return digitos

	@staticmethod
	def gerar(branch = 1): 
		"""
		Gera uma string de dígitos CNPJ válida aleatória. Um parâmetro opcional de número de ramal pode ser fornecido,
		o padrão é 1.
		"""

		branch %= 10000
		branch += int(branch == 0)
		branch = str(branch).zfill(4)
		base = str(randint(0, 99999999)).zfill(8) + branch

		while len(set(base)) == 1: base = str(randint(0, 99999999)).zfill(8) + branch

		gerador = GeradorCnpj()

		return Cnpj(base + gerador.__checksum(base))
