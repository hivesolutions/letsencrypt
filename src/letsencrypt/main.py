#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class LetsEncryptApp(appier.WebApp):

    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(
            self,
            name = "lets_encrypt",
            *args, **kwargs
        )

if __name__ == "__main__":
    app = LetsEncryptApp()
    app.serve()
else:
    __path__ = []
