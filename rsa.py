import random

class RSA(object):
	"""docstring for RSA"""
	def __init__(self, arg):
		super(RSA, self).__init__()
		self.arg = arg
		
	def gen_prime_num(self, max_num):
		isPrime = [True]*(max_num+2)
		res = []
		for p in range(2,max_num):
			if not isPrime[p]:
				continue
			res.append(p)
			for i in range(2*p, max_num, p):
				isPrime[i] = False

		self.pub_key = random.choice(res)
		self.pri_key = random.choice(res)
		while self.pri_key == self.pub_key:
			self.pri_key = random.choice(res)
				
	def gen_rsa_key(self):
		pass

	def encrypt(self, pub_key, message):
		pass

	def decrypt(self, pri_key, encry):
		pass

if __name__ == '__main__':
	result = gen_prime_num(1000)
	print(len(result))