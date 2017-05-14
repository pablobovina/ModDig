# -*- coding: utf-8 -*-


def int_to_byte(n):
    s = list("{0:b}".format(n))
    #print "".join(s)
    a = []
    if len(s)%8 != 0:
        #print 8-((len(s)%8))
        a = ['0' for e in range(8-((len(s)%8)))]
        s = a + s
    #print "".join(s)
    bi = len(s)
    bs = bi-8
    r = []
    while(bs >= 0):
        p = "".join(s[bs:bi])
        r.append(p)
        #print p
        bi = bs
        bs = bs - 8
    r.reverse()
    #print r
    return r

def bytes_to_reg(l,n):
    le = n-len(l)
    e = '00000000'
    a = [e for i in range(le)]
    print a + l
    return a + l

def bytes_reg_to_int_reg(l):
    r = [int(e, 2) for e in l]
    print r
    return r

def int_reg_to_char_reg(l):
    r = [chr(e) for e in l]
    print r
    return r

def sec_to_usec(n):
    f = 10 ** (-6)
    return n * f

def msec_to_usec(n):
    f = 10 ** (-3)
    return n * f

def nsec_to_usec(n):
    f = 10 ** (3)
    return n * f

print int(int_to_byte(32)[0][0:4],2)
print int(int_to_byte(32)[0][4:8],2)
#int_reg = bytes_reg_to_int_reg(bytes_to_reg(int_to_byte(1024),6))
#char_reg = int_reg_to_char_reg(int_reg)

