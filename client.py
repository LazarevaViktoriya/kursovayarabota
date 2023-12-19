"""Модуль для отправки комманд созданному серверу"""
import socket
import pickle

host = '127.0.0.1'
port = 12345


def toBytes(msg, N = 16):
    """Функция преобразования строки в заданное количество байт"""
    data = str(msg)[:N]
    data += "\0" * (N - len(data))
    return bytes(data, encoding='utf-8')


def connect(code):
	"""Функция для подключения к серверу. -> str"""
	global client_socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((host, port))

	client_socket.send(toBytes(code)) #отправка кода сотрудника
	response = client_socket.recv(16).decode('utf-8').strip('\0')
	return response


def disconnect():
	"""Функция для отключения от сервера"""
	global client_socket
	try:
		client_socket.send(toBytes('DISCONNECT'))
		client_socket.close()
	except: pass


def get_table_data(n):
	"""Функция для получения списка блюд на указанном столе. -> list"""
	client_socket.send(toBytes('GETTABLE'))
	client_socket.send(toBytes(n))
	rsize = int(client_socket.recv(16).decode('utf-8').strip('\0'))
	r = client_socket.recv(rsize)
	r = pickle.loads(r) 
	return r


def remove_dish_from_table(D, n):
	"""Функция для отправки команды удаления блюда со стола"""
	client_socket.send(toBytes('REMOVEDISH'))
	client_socket.send(toBytes(n))
	r = pickle.dumps(D)
	rsize = len(r)
	client_socket.send(toBytes(rsize))
	client_socket.send(r)


def add_dish_to_table(D, n):
	"""Функцияя для отпрвки команды добавления указанного блюда на стол"""
	client_socket.send(toBytes('ADDDISH'))
	client_socket.send(toBytes(n))
	r = pickle.dumps(D)
	rsize = len(r)
	client_socket.send(toBytes(rsize))
	client_socket.send(r)


def get_dishes_list():
	"""Функцияя для отправки команды получения списка блюд не в стоп-листе. -> list"""
	client_socket.send(toBytes('GETDISHES'))
	rsize = int(client_socket.recv(16).decode('utf-8').strip('\0'))
	r = client_socket.recv(rsize)
	r = pickle.loads(r) 
	return r


def get_all_dishes_list():
	"""Функцияя для отправки команды получения списка всех блюд. -> list"""
	client_socket.send(toBytes('GETALLDISHES'))
	rsize = int(client_socket.recv(16).decode('utf-8').strip('\0'))
	r = client_socket.recv(rsize)
	r = pickle.loads(r)
	return r


def dish_to_sl(d):
	"""Функцияя для отправки команды добавления блюда в стоп-лист"""
	client_socket.send(toBytes('DISHTOSL'))
	client_socket.send(toBytes(d, 32))


def dish_from_sl(d):
	"""Функцияя для отправки команды удаления блюда из стоп-листа"""
	client_socket.send(toBytes('DISHFROMSL'))
	client_socket.send(toBytes(d, 32))


def product_to_sl(p):
	"""Функцияя для отправки команды добавления блюд в стоп-лист по заданному продукту"""
	client_socket.send(toBytes('PRODTOSL'))
	client_socket.send(toBytes(p, 32))


if __name__ == "__main__":
	pass