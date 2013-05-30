# -*- coding: utf-8 -*-
"""
Simple python API to Singly
created by venelin@magicsolutions.bg
"""
import logging
import slumber
from urllib import urlencode


logger = logging.getLogger(__name__)

API_BASE_URL = 'https://api.singly.com/v0/'


def get_singly_authentication_url(service, client_id, redirect_uri, access_token=None, scope=None):
    """
    Get url that user must open to authenticate with given service trough singly

    service  - service to authenticate against e.g. 'twitter' or 'facebook'
    redirect_uri -  this is a callback URL where you will receive authentication code
    """

    # Format of authenticate URL:
    # https://api.singly.com/oauth/authenticate?client_id=CLIENT-ID&
    #   redirect_uri=REDIRECT-URI&service=SERVICE
    params = {
        'service': service,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    }
    if access_token:
        params['access_token'] = access_token
    if scope:
        params['scope'] = ','.join(scope)
    return '%soauth/authenticate?%s' % (API_BASE_URL, urlencode(params))


def singly_authenticate(client_id, client_secret, code, **params):
    """
    Try to authenticate with returned code
    This code must be obtained from a callback url to wich
    a user will be redirected after successfull authentication

    """
    params.update({
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code
    })

    api = SinglyAPI()
    logger.debug("Trying to get access token with this params %s" % (params,))
    response = api.oauth.access_token.post(params)
    logger.debug("Access token response data is %s" % (response, ))

    # Expect
    # {
    # "access_token": "S0meAcc3ssT0k3n"
    # }
    access_token = response.get('access_token')
    logger.debug("Access token is %s" % (access_token, ))

    if not access_token:
        return

    return SinglyAPI(**response)


class ResourceAttributesMixin(slumber.ResourceAttributesMixin):
    """
    Wrapper over slumber.ResourceAttributesMixin whicl will return
    Singly Resource, not a defailt resource

    """

    def __getattr__(self, item):
        # NOTE: Original method is very simple, and mey be there is no
        # need of calling super. We can doid by our self. But for now is ok.
        resource = super(ResourceAttributesMixin, self).__getattr__(item)
        return Resource(**resource._store)


class Resource(ResourceAttributesMixin, slumber.Resource):
    """
    Wrapper over slumber.Resource. This wrapper will pass
    access_token if it is provided to all requests to Singly API.

    Singly API accept only GET and POST methods for now

    """

    def _get_kwargs(self, kwargs):
        """
        Simple metod which will try to add access_token to the kwargs

        """

        if self._store.get('access_token'):
            kwargs['access_token'] = self._store['access_token']
        return kwargs

    def get(self, **kwargs):
        return super(Resource, self).get(**self._get_kwargs(kwargs))

    def post(self, data, **kwargs):
        return super(Resource, self).post(data, **self._get_kwargs(kwargs))


class SinglyAPI(ResourceAttributesMixin, slumber.API):
    """
    Wrapper over slumber.API which will automatically create resources
    which will automatically send access token to every request.

    """

    def __init__(self, **kwargs):
        super(SinglyAPI, self).__init__(API_BASE_URL, append_slash=False)
        self._store.update(kwargs)

    def get_access_token(self):
        return self._store.get('access_token')

    def get_account(self):
        return self._store.get('account')

    def get_profile(self):
        return self._store.get('profile') or {}


class Singly(object):
    """
    Simple object that can be initialized in the begiinig of the app
    with required settings:

    app_key - application key provided from Singly
    app_secret - application secred provided from singly
    redirect_uri - URI to which singly will redirect a user after successfull
                authentication with some service. On this address singly will
                send a code, needed for your application to authenticate with
                Singly.
    """

    def __init__(self, app_key, app_secret, redirect_uri, default_scopes=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.redirect_uri = redirect_uri
        self.default_scopes = default_scopes or {}

    def get_authentication_url(self, service, access_token=None, scope=None, next_url=None):
        """
        Wrapper over get_singly_authentication_url

        """
        scope = scope or self.default_scopes.get(service, [])
        redirect_uri = self.redirect_uri
        if next_url:
            redirect_uri = '%s?%s' % (redirect_uri, urlencode({'next': next_url}))
        return get_singly_authentication_url(service, self.app_key, redirect_uri, access_token, scope)

    def authenticate(self, code, **kwargs):
        """
        wrapper over singly_authenticate function

        """
        return singly_authenticate(self.app_key, self.app_secret, code, **kwargs)
