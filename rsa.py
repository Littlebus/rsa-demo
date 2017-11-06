import random


def str2int(message):
	total = 0
	for x in message:
		total = total << 8 | ord(x)
	return total

def int2str(number):
	mask = 255
	res = []
	while number != 0:
		res.append(chr(number & mask))
		number >>= 8
	return ''.join(res[::-1])

class RSA(object):
	"""docstring for RSA"""
	def __init__(self):
		super(RSA, self).__init__()
		
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
		a = a % c
		ans = 1
		while b != 0:
			if b & 1 == 1:
				ans = (ans * a) % c
			b >>= 1
			a = (a * a) % c
		return ans

	def gen_rsa_key(self):
		"""返回tuple，其中第一个tuple为公钥"""
		res = self.gen_prime_num(10000)
		p = random.choice(res)
		q = random.choice(res)
		while p == q:
			p = random.choice(res)
		n = p * q
		r = (p - 1) * (q - 1)
		r_prime = self.gen_prime_num(r)
		e = random.choice(r_prime)
		d = 0
		for x in range(2,r):
			if x * e % r == 1:
				d = x
				break
		return ((e,n),(d,n))

	def encrypt(self, message, e, n):
		return self.quick(message, e, n)

	def decrypt(self, encry, d, n):
		return self.quick(encry, d, n)

	def ca_sign(self):
		content = input('input sign message:')



if __name__ == '__main__':
	m = input('input message:')
	rsa_sample = RSA()
	key = rsa_sample.gen_rsa_key()
	print('密钥大小为:',key[0][1])
	cipher = rsa_sample.encrypt(21312321, *(key[0]))
	text = rsa_sample.decrypt(cipher, *(key[1]))
	print(text)
	# encrypt_text = rsa_sample.encrypt(str2int(m), *(key[0]))
	# print('encrypt_text', encrypt_text)
	# print('encrypted text :',encrypt_text)
	# decrypt_text = int2str(rsa_sample.decrypt(encrypt_text, *(key[1])))
	# print('decrypted text :',decrypt_text)
