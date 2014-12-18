#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libbls import createParser, StartingError, ApplicationError, checkMethods, strToList
from classbls import BLS
import sys, pickle, os

from charm.core.engine.util import serializeObject, serializeDict, deserializeObject, deserializeDict

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])
	
	bls = BLS(namespace.params, namespace.debug)
	method = checkMethods(namespace)
	if method == 1:
		raise StartingError('Не был выбран метод работы программы')
	elif method == 2:
		raise StartingError('Был выбран больше, чем один метод работы программы')
	elif method == 'k':
		(pk, sk) = bls.keygen()
		try:
			os.mkdir(namespace.directory)
		except IOError:
			pass
		f1 = open(namespace.directory + namespace.public_key, 'wb')
		f1.write(str(serializeDict(pk, bls.group)))
		f1.close()
		f2 = open(namespace.directory + namespace.secret_key, 'wb')
		f2.write(str(serializeObject(sk, bls.group)))
		f2.close()
	elif method == 's':
		try:
			f1 = open(namespace.directory + namespace.secret_key, 'rb')
			sk = deserializeObject(f1.read(), bls.group)
		except IOError:
			raise ApplicationError('Файла с закрытым ключом по указанному пути не существует')
		f1.close()
		if namespace.message == None and namespace.file == None:
			raise StartingError('Не было указано сообщение или путь файла с сообщением')
		elif namespace.message != None and namespace.file != None:
			raise StartingError('Были указаны 2 вида сообщений')
		elif namespace.message != None:
			message = namespace.message
		elif namespace.file != None:
			try:
				f2 = open(namespace.file, 'rb')
				message = f2.read()
			except IOError:
				raise ApplicationError('Файла с сообщением по указанному пути не существует')
			f2.close()
		sign = bls.sign({'message': message}, sk)
		f3 = open(namespace.directory + namespace.signature, 'wb')
		f3.write(str(serializeObject(sign, bls.group)))
	elif method == 'v':
		try:
			f1 = open(namespace.directory + namespace.public_key, 'rb')
			pk = deserializeDict(eval(f1.read()), bls.group)
		except IOError:
			raise ApplicationError('Файла с открытым ключом по указанному пути не существует')
		f1.close()
		try:
			f2 = open(namespace.directory + namespace.signature, 'rb')
			sign = deserializeObject(f2.read(), bls.group)
		except IOError:
			raise ApplicationError('Файла с цифровой подписью по указанному пути не существует')
		f2.close()
		if namespace.message == None and namespace.file == None:
			raise StartingError('Не было указано сообщение или путь файла с сообщением')
		elif namespace.message != None and namespace.file != None:
			raise StartingError('Были указаны 2 вида сообщений')
		elif namespace.message != None:
			message = namespace.message
		elif namespace.file != None:
			try:
				f3 = open(namespace.file, 'rb')
				message = f3.read()
			except IOError:
				raise ApplicationError('Файла с сообщением по указанному пути не существует')
			f3.close()
		result = bls.verify({'message': message}, sign, pk)
		if result:
			print '\nПРОВЕРКА ПРОШЛА УСПЕШНА!\n'
		else:
			print '\nПРОВЕРКА НЕ ПРОЙДЕНА!\n'