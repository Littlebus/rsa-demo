import random

class RSA(object):
	"""docstring for RSA"""
	def __init__(self):
		super(RSA, self).__init__()
		self.gen_rsa_key()
		
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

	def quick(self, a, b, c):
		"""(a^b)%c的快速幂取模"""
		ans = 1
		while b != 0:
			if b&1 == 1:
				ans = (ans * a) % c
			b >>= 1
			a = (a * a) % c
		return ans

	def gen_rsa_key(self):
		"""返回tuple，其中第一个tuple为公钥"""
		res = self.gen_prime_num(1000)
		p = random.choice(res)
		q = random.choice(res)
		while p == q:
			p = random.choice(res)
		self.n = p * q
		r = (p - 1) * (q - 1)
		r_prime = self.gen_prime_num(r)
		self.e = random.choice(r_prime)
		d = 0
		for x in range(2,r):
			if x * self.e % r == 1:
				d = x
				break
		self.d = d

	def encrypt(self, message):
		return self.quick(message, self.e, self.n)

	def decrypt(self, encry):
		return self.quick(encry, self.d, self.n)

if __name__ == '__main__':
	m = input('input message:')
	rsa_sample = RSA()
	encrypt_text = [rsa_sample.encrypt(ord(x)) for x in m]
	print('encrypted text :',encrypt_text)
	decrypt_text = [chr(rsa_sample.decrypt(x)) for x in encrypt_text]
	print('decrypted text :',''.join(decrypt_text))
