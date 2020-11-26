#!usr/bin
import RSAencryption as RSAenc
import base64

from Crypto.PublicKey import RSA


def main():

    msg = str(input("Enter a message to cipher: "))

    e, d, n = RSAenc.generateKeys()

    print("ENC: \t", e)
    print("DEC: \t", d)
    print("N: \t", n)

    # e = bytes("""MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDmahtsq9iDJk+gvX+LeKdgJqSAWxgnzCycUpWO6p5I3JOe0vrwsjmNffBOC9KmMaRAZGfL6G7K3Fp1I5nrvEnbu+EPrZZ64nt3sg0olrI9VFPby5gGILCAp6UnYkLe6TqjHiufXlIkcLdPfrid/cYJw279JVkNTt3cg2lMZ66MawIDAQAB""", "utf-8")
    # d = bytes("""MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOZqG2yr2IMmT6C9f4t4p2AmpIBbGCfMLJxSlY7qnkjck57S+vCyOY198E4L0qYxpEBkZ8vobsrcWnUjmeu8Sdu74Q+tlnrie3eyDSiWsj1UU9vLmAYgsICnpSdiQt7pOqMeK59eUiRwt09+uJ39xgnDbv0lWQ1O3dyDaUxnroxrAgMBAAECgYBhE/uSAaUrPIz4EF8YiDEc1ashWUAIJIH3KuRQXpFp6WVY2VNY7f5JmvIQL/MEio3Fg4gn5TooxkZmbCWBqMcEvJBg6IQUs+xlfIc11GS2wH9vsPkAkttb5d78CXv7r0Lx3eHzmmBONa8i36LfD/s/usST0Ksci3CnWSEY/AuvwQJBAPt270eOOt0UwH1IOor7SLJ+IjOJzuD6wwUY2CibBxcUelPhr61xkZLmBMzwQDmo15J7KXGJeM1BCyDS1abhXlMCQQDqkfrJJvIH1rNEOjV5zCOlJvon3bGhuiDdJzv5PP1IuTqx2ezCFe8dxvoVFLytlPJ/PJn8bxKlnH7RD5CgymaJAkEAjAED58sAauaK5TW5oneVWgtv71HipM/4lHXoo3Ls16THFryomuCINElsks2QdInUu/FmeZgYce6sy3GXEnqXkQJAYfHkeruVUiqXHgUEMUBJHfvBdoX+Vt5mPJHWXALYa9ZUKNErJ/uKpa9g2w6WnhBUlUZTsfEbIyXOWjMam9kHqQJAdLuqw6bDsaeeGmccSP2a2UKYjpC8a/FG5tAxZD9EvtZSh+ets/jJ5OiZE0uuVLcfWWSSBpUVuwLXo6NnuJOYMA==""", "utf-8")
    
    # e = int.from_bytes(e,  byteorder='big')

    # d = int.from_bytes(d, byteorder='big')

    # keypairs = RSA.generate(bits = 1024)

    # e = keypairs.e
    # d = keypairs.d
    # n = keypairs.n

    # print("String chave E: \t", e)
    # print("String chave D: \t", d)
    # print("String chave N: \t", n)




    msgcifrada = RSAenc.encrypt(msg, e, n)
    
    print("Mensagem cifrada : ", msgcifrada)

    msgdecifrada = RSAenc.decrypt(msgcifrada, d, n)

    print("Mensagem decifrada : ", msgdecifrada)

if __name__ == '__main__':
    main()