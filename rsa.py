#coding:utf-8

import random
import math
import sys, os

__author__ = 'Kecheng Xiao'
__version__ = 'version 1.0'


def str2int(message):
    '''
    将字符串简单映射为整数

    :param message: 字符串
    :returns: 整数
    '''
    total = 0
    for x in message:
        total = total << 8 | ord(x)
    return total

def int2str(number):
    '''
    将整数转换为字符串
    
    :param number: 待转换的整数
    :returns: 转换完的字符串
    '''
    mask = 255
    res = []
    while number != 0:
        res.append(chr(number & mask))
        number >>= 8
    return ''.join(res[::-1])

def exgcd(a, b):
    '''
    扩展欧几里得算法求ax+by=gcd(a,b)的一组特解

    :param a: 系数a
    :param b: 系数b
    :returns: 特解(x0,y0)
    '''
    if b == 0:
        return (1,0)
    else:
        res = exgcd(b, a%b)
        return (res[1], res[0] - a // b * res[1])

def gcd(a, b):
    '''
    欧几里得算法求gcd(a,b)

    :param a: a
    :param b: b
    :returns: gcd(a,b)
    '''
    if b == 0:
        return a
    else:
        return gcd(b,a%b)

class RSA(object):
    '''
    RSA类，包含了RSA相关的方法
    '''
    def __init__(self):
        super(RSA, self).__init__()
        
    def gen_prime_num(self, min_num, max_num):
        '''
        用素数筛选法生成素数,此方法只能产生较小范围的素数
        
        :param min_num: 素数的下界
        :param max_num: 素数的上界
        :returns: 素数列表
        '''
        isPrime = [True]*(max_num+2)
        res = []
        for p in range(2,max_num):
            if not isPrime[p]:
                continue
            if p > min_num:
                res.append(p)
            for i in range(2*p, max_num, p):
                isPrime[i] = False

        return res

    def quick(self, a, b, c):
        '''
        (a^b)%c的快速模幂运算
        
        :param a: 底数
        :param b: 指数
        :param c: 模数
        :returns: 运算结果
        '''
        a = a % c
        ans = 1
        while b != 0:
            if b & 1 == 1:
                ans = (ans * a) % c
            b >>= 1
            a = (a * a) % c
        return ans

    def gen_rsa_key(self):
        '''
        生成rsa的密钥对

        :returns: 一个tuple,tuple中有两个tuple分别是公钥和私钥:(e,n)(d,p,q)
        '''
        res = self.gen_prime_num(500000,1000000)
        p = random.choice(res)
        q = random.choice(res)
        while p == q:
            p = random.choice(res)
        print('p:',p,'q:',q)
        n = p * q
        print('n:',n,'log n :',math.log(n))
        r = (p - 1) * (q - 1)
        r_prime = self.gen_prime_num(65537,100000)
        e = 65537 #2^16+1
        while gcd(e, r) != 1:
            e = random.choice(r_prime)
        '''
        扩展欧几里得求e模\phi(n)的乘法逆元
        '''
        res = exgcd(e, r)
        d = res[0]
        d = d - d//r * r
        # print('逆元运算：',d * e % r)
        return ((e,n),(d,p,q))

    def encrypt(self, message, e, n):
        '''
        加密

        :param message: 明文
        :param e: 密钥
        :param n: 模数
        :returns: 密文
        '''
        return self.quick(message, e, n)

    def decrypt(self, encry, d, n):
        '''
        解密
        
        :param encry: 被加密的密文
        :param d: 密钥
        :param n: 模数
        :returns: 解密的整数
        '''
        return self.quick(encry, d, n)

    def ca_sign(self):
        '''
        用来生成随机密钥对并且签发CA证书，生成在本地目录
        '''
        m = input('输入你的姓名（签字内容，姓名首字母，5个字符以内）')
        key = self.gen_rsa_key()
        pri_path = input('输入私钥生成文件名 [rsa_key.pri]')
        if pri_path == '':
            pri_path = 'rsa_key.pri'
        if os.path.exists(pri_path):
            isOverwrite = input('文件存在，是否覆盖? [y/n] [y]')
            if isOverwrite == 'n':
                return
        with open(pri_path, 'w') as f:
            f.write(str(key[1][0])+'\n')
            f.write(str(key[1][1])+'\n')
            f.write(str(key[1][2]))

        pub_path = input('输入公钥生成文件名 [rsa_key.pub]')
        if pub_path == '':
            pub_path = 'rsa_key.pub'
        if os.path.exists(pub_path):
            isOverwrite = input('文件存在，是否覆盖? [y/n] [y]')
            if isOverwrite == 'n':
                return
        with open(pub_path, 'w') as f:
            f.write(str(key[0][0])+'\n')
            f.write(str(key[0][1])+'\n')
            print("pub key",key[0])
            encrypt_text = self.encrypt(str2int(m), key[1][0], key[0][1])
            f.write(str(encrypt_text))
        
    def validation(self, pubPath):
        '''
        用于CA客户端验证证书是否有效

        :param pubPath: 公钥的路径
        '''
        if not os.path.exists(pubPath):
            print('文件不存在!')
            return
        with open(pubPath, 'r') as f:
            pub_key = (int(f.readline()),int(f.readline()))
            message = int(f.readline())
            # os.getcwd()
            # os.path.walk(os.getcwd(), self.cb, pub_key)
            files = os.listdir(os.getcwd())
            for file in files:
                if os.path.isfile(file):
                    # print os.path.splitext(file)
                    if os.path.splitext(file)[1] == '.pri':
                        with open(file) as f:
                            pri_key = (int(f.readline()),int(f.readline()),int(f.readline()))
                            if pri_key[0] * pub_key[0] % ((pri_key[1] - 1) * (pri_key[2] - 1)) == 1:
                                n = pri_key[1] * pri_key[2]
                                print('confirmed , sign content : ')
                                print(int2str(self.decrypt(message, *(pub_key))))
                                return
            print('invalid key')
