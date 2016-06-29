#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import base64
import hashlib

import appier

class BaseController(appier.Controller):

    @appier.route("/", "GET")
    def index(self):
        thumbprint = self.jwk_thumbprint()
        return dict(
            thumbprint = thumbprint
        )

    def jwk_thumbprint(self, account_key = None):
        account_key = account_key or self._account_key()
        jwk = self._header(account_key)["jwk"]
        as_json = json.dumps(jwk, sort_keys = True, separators = (",", ":"))
        as_json = as_json.encode("utf-8")
        hash = hashlib.sha256(as_json)
        result = hash.digest()
        return self._jose_b64(result)

    def _account_key(self, encoding = "utf-8"):
        file = open("C:/repo.extra/letsencrypt/src/letsencrypt/private_key.json", "rb")
        try: data = file.read()
        finally: file.close()
        data = data.decode(encoding)
        account_key = json.loads(data)
        return account_key

    def _header(self, account_key):
        return dict(
            alg = "RS256",
            jwk = dict(
                kty = account_key["kty"],
                e = account_key["e"],
                n = account_key["n"],
            )
        )

    def _jose_b64(self, data):
        return base64.urlsafe_b64encode(data).decode("ascii").replace("=", "")
