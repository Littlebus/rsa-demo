import random

class RSA(object):
	"""docstring for RSA"""
	def __init__(self):
		super(RSA, self).__init__()
		gen_rsa_key()
		
	def gen_prime_num(self, max_num):
		isPrime = [True]*(max_num+2)
		res = []
		for p in range(2,max_num):
			if not isPrime[p]:
				continue
			res.append(p)
			for i in range(2*p, max_num, p):
				isPrime[i] = False

		return res
				
	def gen_rsa_key(self):
		"""返回tuple，其中第一个tuple为公钥"""
		res = gen_prime_num(10000)
		self.p = random.choice(res)
		self.q = random.choice(res)
		while self.p == self.q:
			self.p = random.choice(res)
		self.n = self.p * self.q
		r = (p - 1) * (q - 1)
		r_prime = gen_prime_num(r)
		self.e = random.choice(r_prime)
		self.d = 0
		for x in range(2,r):
			if x * e % r == 1:
				self.d = x
				break

	def encrypt(self, message):
		return (message**self.e)%self.n

	def decrypt(self, encry):
		return (encry**self.d)%self.n

if __name__ == '__main__':
	m = input('input message:')
	rsa_sample = RSA(m)
	encrypt_text = [rsa_sample.encrypt(ord(x)) for x in m]
	print(encrypt_text)
	decrypt_text = [chr(rsa_sample.decrypt(x)) for x in encrypt_text]
	print(decrypt_text)
