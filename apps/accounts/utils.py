from hashlib import sha512

def make_hash(passwd):
	try:
		h = sha512(passwd)
		return h.hexdigest()
	except Exception, e:
		raise e

