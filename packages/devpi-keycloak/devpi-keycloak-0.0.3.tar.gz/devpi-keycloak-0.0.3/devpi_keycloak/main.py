# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import argparse

try:
    from devpi_server.auth import AuthException
    from devpi_server.log import threadlog

except ImportError:  # No devpi_server available
    class AuthException(Exception):
        pass

    import logging
    threadlog = logging

from keycloak import Keycloak, Token

keycloak_url = None
keycloak_realm = None

def devpiserver_auth_request(userdict, username, password):
    global keycloak_url
    global keycloak_realm

    service: Keycloak = Keycloak(
        keycloak_url,
        keycloak_realm,
        "admin-cli"
    )
    
    try:
        token: Token = service.auth(username,password)
        if (token.check_auth()):
            token.logout()
            threadlog.info("kc-auth '%s' authenticate",username)
            return {"status":"ok"}
        else:
            threadlog.exception("kc-auth failed to authenticate")
            return None
    except:
        threadlog.exception("kc-auth failed to authenticate")
        return None

class KeycloakConfigUrl(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global keycloak_url
        keycloak_url = values
        setattr(namespace, self.dest, keycloak_url)

class KeycloakConfigRealm(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global keycloak_realm
        keycloak_realm = values
        setattr(namespace, self.dest, keycloak_realm)


def devpiserver_add_parser_options(parser):
    gitlab = parser.addgroup("Keycloak auth")
    gitlab.addoption("--kc-url", action=KeycloakConfigUrl, help="Keycloak URL")
    gitlab.addoption("--kc-realm", action=KeycloakConfigRealm, help="Keycloak realm name")

