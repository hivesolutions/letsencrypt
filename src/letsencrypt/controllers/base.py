#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import base64

import appier

class BaseController(appier.Controller):

    @appier.route("/", "GET")
    def index(self):
        #import manuale.account

        #file = open("C:/Users/joamag/workspace/letsencrypt/src/letsencrypt/private_key.json", "rb")
        #try: data = file.read()
        #finally: file.close()

        #key = manuale.account.deserialize(data)
        #print(key)

        account_key = self._get_account_key()
        thumbprint = self.generate_jwk_thumbprint(account_key)
        return dict(
            thumbprint = thumbprint
        )

    def _get_account_key(self, encoding = "utf-8"):
        file = open("C:/Users/joamag/workspace/letsencrypt/src/letsencrypt/private_key.json", "rb")
        try: data = file.read()
        finally: file.close()
        data = data.decode(encoding)
        account_key = json.loads(data)
        return account_key

    def jose_b64(self, data):
        return base64.urlsafe_b64encode(data).decode("ascii").replace("=", "")

    def generate_header(self, account_key):
        #numbers = account_key.public_key().public_numbers()
        #e = numbers.e.to_bytes((numbers.e.bit_length() // 8 + 1), byteorder = "big")
        #n = numbers.n.to_bytes((numbers.n.bit_length() // 8 + 1), byteorder = "big")
        #if n[0] == 0: n = n[1:]
        return dict(
            alg = "RS256",
            jwk = dict(
                kty = "RSA",
                e = account_key["e"],
                n = account_key["n"],
            )
        )

    def generate_jwk_thumbprint(self, account_key):
        jwk = self.generate_header(account_key)["jwk"]
        as_json = json.dumps(jwk, sort_keys = True, separators = (",", "':"))
        as_json = as_json.encode("utf-8")
        #@todo tenho de gerar o hash aki !!!

        import hashlib
        hash = hashlib.sha256()
        hash.update(as_json)
        result = hash.digest()
        return self.jose_b64(result)
