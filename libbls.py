#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

version = '1.0.0'

def createParser():
	"""Параметры запуска скрипта
	
	Функция вызывается при запуске основного скрипта sigbls.py
	
	Аргументы:
		Вспомогательные параметры:
			-h, --help							справка
			-v, --version						номер версии
			
		Основные параметры:
			необходимо указать один из основных параметров
			
			-m [MESSAGE], --message [MESSAGE]				сообщение, на основании которого
															необходимо  создать цифровую
															подпись.
			-f [FILE], --file [FILE]						путь до файла с сообщением.
			-p {SS512,SS1024,MNT159,MNT201,MNT224},			параметры эллиптической
			--params {SS512,SS1024,MNT159,MNT201,MNT224}	кривой.
			
		Второстепенные параметры:
			-d, --debug										вывод подробной ифнормации.
	
	Исключения:
		StartingError: Возникает при неправильном запуске скрипта.
	"""
	
	parser = argparse.ArgumentParser(
		prog = 'ЭЦП БЛС',
		description = 'Данная программа является реализацией асимметричной криптосхемы Боне-Линна-Шахема на основе парных отображений.',
		epilog = '(c) МИФИ, 2014. Пак Михаил, Волков Дмитрий.',
		add_help = False
	)
	
	info_group = parser.add_argument_group(title = 'Вспомогательная информация')
	info_group.add_argument('-h', '--help', action = 'help', help = 'справка')
	info_group.add_argument(
		'--version',
		action = 'version',
		help = 'номер версии',
		version = '%(prog)s {}'.format(version)
	)
	
	method_group = parser.add_argument_group(
		title = 'Методы',
		description = 'можно выбрать только один из методов работы программы'
	)
	method_group.add_argument(
		'-k',
		action = 'store_const',
		const = True,
		default = False,
		help = 'генерация ключа.'
	)
	method_group.add_argument(
		'-s',
		action = 'store_const',
		const = True,
		default = False,
		help = 'формирование подписи.'
	)
	method_group.add_argument(
		'-v',
		action = 'store_const',
		const = True,
		default = False,
		help = 'проверка подписи.'
	)
	
	main_group = parser.add_argument_group(
		title = 'Основные параметры'
	)
	main_group.add_argument(
		'-m',
		'--message',
		help = 'сообщение, на основании которого необходимо создать цифровую подпись.'
	)
	main_group.add_argument(
		'-f',
		'--file',
		help = 'путь до файла с сообщением.'
	)
	main_group.add_argument(
		'-d',
		'--directory',
		default = 'keys/',
		help = 'путь до каталога, где хранятся (или будут храниться) ключи и подписи.'
	)
	main_group.add_argument(
		'--public-key',
		default = 'public.key',
		help = 'имя файла с публичным ключом.'
	)
	main_group.add_argument(
		'--secret-key',
		default = 'secret.key',
		help = 'имя файла с секретным ключом.'
	)
	main_group.add_argument(
		'--signature',
		default = 'signature.key',
		help = 'имя файла с цифровой подписью.'
	)
	main_group.add_argument(
		'-p',
		'--params',
		choices = ['SS512', 'SS1024', 'MNT159', 'MNT201', 'MNT224'],
		default = 'SS512',
		help = 'параметры эллиптической кривой.'
	)
	
	minor_group = parser.add_argument_group(title = 'Второстепенные параметры')
	minor_group.add_argument(
		'--debug',
		action = 'store_const',
		const = True,
		default = False,
		help = 'Вывод подробной ифнормации функционирования алгоритма.'
	)
	
	return parser


class Error(Exception):
	"""Базовый класс исключений"""
	pass
 
class StartingError(Error):
	"""Неправильный ввод аргументов при запуске	
	Возникает при неправильном запуске скрипта.
 
	Атрибуты:
		message			объяснение ошибки
	"""
	def __init__(self, message):
		self.message = message
 
class ApplicationError(Error):
	"""Возникает при внутренней ошибке приложения.
 
	Атрибуты:
		message 		объяснение ошибки
	"""
	def __init__(self, message):
		self.message = message

def checkMethods(namespace):
	"""Проверка количества методов, веденные с консоли
	
	Результат:
		False				если количество методов не равно единице.
		methodSymbol		символьное обозначение метода.
	"""
	i = 0
	methodSymbol = ''
	if namespace.k:
		i+=1
		methodSymbol += 'k'
	if namespace.s:
		i+=1
		methodSymbol += 's'
	if namespace.v:
		i+=1
		methodSymbol += 'v'
	if i == 0:
		return 1
	elif i > 1:
		return 2
	return methodSymbol
	
def strToList(str):
	"""Преобразование строки в список
	
	Аргументы:
		str		строка
	
	Результат:
		list	список
	"""
	array = str.split(',')
	list = []
	list.append(int(array[0][1:]))
	list.append(int(array[1][:-1]))
	return list