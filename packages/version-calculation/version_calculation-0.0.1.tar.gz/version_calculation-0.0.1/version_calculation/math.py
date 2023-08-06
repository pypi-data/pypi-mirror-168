from collections import Counter
class Error(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'calError, {0} '.format(self.message)


class cal:
	def __init__(self,numero,casas=None):
		self.__numero = numero
		my_str = self.__numero
		counter = Counter(my_str)
		num = counter['.']

		casnum = 100
		if casas != None:
			if type(casas) == int and not casas < 2:
				casnum = 10
				x = 1
				while x < casas:
					casnum = casnum * 10
					x += 1
			else:
				raise Error('o numero de casas deve ser um int com no minimo 2 casas')

		self.__casnum = casnum
		if num == 2:
			self.__strnumero = self.__numero.replace(' ', '')
			self.__strnumero = self.__strnumero.split('.')

			self.__strnumero[0] = (self.__strnumero[0], 0)[self.__strnumero[0] == None or self.__strnumero[0] == '']
			self.__strnumero[1] = (self.__strnumero[1], 0)[self.__strnumero[1] == None or self.__strnumero[1] == '']
			self.__strnumero[2] = (self.__strnumero[2], 0)[self.__strnumero[2] == None or self.__strnumero[2] == '']

			self.__strnumero[1] = (int(self.__strnumero[1])*100, 0)[int(self.__strnumero[1]) == 0]
			self.__strnumero[0] = (int(self.__strnumero[2])*1000, 0)[int(self.__strnumero[2]) == 0]
			self.__strnumero = self.__strnumero[0] + self.__strnumero[1] + self.__strnumero[2]
		else:
			raise Error('as versoes devem seguir o padrao numero.numero.numero')

	def __dhome(self,x:int):
		y = 0
		while x == self.__casnum or x > self.__casnum:
			x = x - self.__casnum
			y += 1
		self.__x = int(x)
		self.__y = int(y)

	def calculo(self,calculo:str):
		re = calculo.replace('n',str(self.__strnumero))
		re = int(eval(re))
		self.__dhome(re)
		C3 = self.__x
		y = self.__y
		self.__dhome(y)
		C2 = self.__x
		C1 = self.__y
		return f'{C1}.{C2}.{C3}'