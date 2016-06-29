#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import base64
import hashlib

import appier

class BaseController(appier.Controller):

    @appier.route("/.well-known/acme-challenge/<str:token>", "GET")
    def challenge(self, token):
        thumbprint = self.jwk_thumbprint()
        return "%s.%s" % (token, thumbprint)

    def jwk_thumbprint(self, account_key = None):
        account_key = account_key or self._account_key()
        jwk = self._header(account_key)["jwk"]
        jwk_j = json.dumps(jwk, sort_keys = True, separators = (",", ":"))
        jwk_j = jwk_j.encode("utf-8")
        hash = hashlib.sha256(jwk_j)
        result = hash.digest()
        return self._jose_b64(result)

    def _account_key(self, account = None, encoding = "utf-8"):
        le_path = appier.conf("LE_PATH", "/etc/letsencrypt")
        accounts_path = os.path.join(
            le_path,
            "accounts",
            "acme-v01.api.letsencrypt.org",
            "directory"
        )
        accounts_path = os.path.normpath(accounts_path)
        if not account: account = os.listdir(accounts_path)[0]
        account_path = os.path.join(accounts_path, account)
        file_path = os.path.join(account_path, "private_key.json")
        file = open(file_path, "rb")
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
