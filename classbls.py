#!/usr/bin/env python
# -*- coding: utf-8 -*-

from charm.toolbox.pairinggroup import PairingGroup, G1, G2, pair
from charm.core.engine.util import objectToBytes
from hashlib import sha256

class BLS():
	"""Класс, реализующий формирование и проверку ЭЦП по схеме Боне-Линна-Шахема
	
	Атрибуты:
		debug			вывод дополнительной информации.
		group			содержит в себе данные об точках на эллиптической кривой, 
						порядке множества точек эллиптической кривой и так далее.
		P				произвольная точка эллиптической кривой.
		sk				секретный ключ.
		pk				публичный ключ.
		
	"""
	
	def __init__(self, param_id, debug):
		"""Конструктор класс
		
		Атрибуты:
			param_id		параметры эллиптической кривой:
							{SS512, SS1024, MNT159, MNT201, MNT224}.
			debug			вывод дополнительной информации.	
		"""
		self.group = PairingGroup(param_id)
		self.debug = debug
	
	def keygen(self):
		"""Генерация ключей
		
		Результат:
			P				произвольная точка эллиптической кривой.
			sk				секретный ключ.
			pk				публичный ключ.
		"""
		P = self.group.random(G2)
		sk = self.group.random()
		pk = {'P^sk': P ** sk, 'P':P}
		if self.debug: self.output(1, sk, pk)
		return (pk, sk)
		
	def sign(self, message, sk):
		"""Формирование подписи
		
		Аргументы:
			message			сообщение, на основании
                        	которого необходимо создать
							цифровую подпись.
			sk				секретный ключ.
		
		Результат:
			sign			цифровая подпись.
		"""
		messageBytes = objectToBytes(message, self.group)
		sign = self.group.hash(messageBytes, G1) ** sk
		if self.debug: self.output(2, 0, 0, message, sign)
		return sign
	
	def verify(self, message, sign, pk):
		"""Проверка подписи
		
		Аргументы:
			message			сообщение, на основании
                        	которого необходимо создать
							цифровую подпись.
			sign			цифровая подпись.
			pk				публичный ключ.
		
		Результат:
			True			при успешной проверки цифровой подписи.
			Fase			при неудачной проверки цифровой подписи.
		"""
		messageBytes = objectToBytes(message, self.group)
		h = self.group.hash(messageBytes, G1)
		ver = pair(sign, pk['P']) == pair(h, pk['P^sk'])
		if self.debug: self.output(3, 0, pk, message, sign, ver)
		if ver:
			return True
		return False
	
	def output(self, phase, sk=0, pk=0, message='', sign=0, ver=False):
		"""Режим дебага
		
		Аргументы:
			type	1	этап генерации ключей.
					2	этап формирования подписи.
					3	этап проверки подписи.
		
		Результат:
			вывод на экран полной информации о работе программы.
		"""
		if phase == 1:
			title = 'ГЕНЕРАЦИЯ КЛЮЧЕЙ'
			out = 'Точка эллиптической кривой:\n' + str(pk['P']) + '\nСекретный ключ:\n' + str(sk) + '\nПубличный ключ:\n' + str(pk['P^sk'])   
		elif phase == 2:
			title = 'ФОРМИРОВАНИЕ ПОДПИСИ'
			out = 'Сообщение:\n' + str(message) + '\nЦифровая подпись:\n' + str(sign)
		elif phase == 3:
			title = 'ПРОВЕРКА ПОДПИСИ'
			out = 'Публичный ключ:\n' + str(pk['P^sk']) + '\nСообщение:\n' + str(message) + '\nЦифровая подпись:\n' + str(sign) + '\nПроверка:'
			if ver: out += 'Успешно'
			else: out += 'Неудачно'
		else: return
		print '=========={0}==========\n{1}'.format(title, out)
		print '=======================================\n'