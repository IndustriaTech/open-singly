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


def get_authentication_url(service, client_id, redirect_uri):
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
    return '%soauth/authenticate?%s' % (API_BASE_URL, urlencode(params))


class ResourceAttributesMixin(slumber.ResourceAttributesMixin):
    def __getattr__(self, item):
        resource = super(ResourceAttributesMixin, self).__getattr__(item)
        return Resource(**resource._store)


class Resource(ResourceAttributesMixin, slumber.Resource):
    """
    Singly API accept only GET and POST methods for now

    """

    def _get_kwargs(self, kwargs):
        if self._store.get('singly_access_token'):
            kwargs['access_token'] = self._store['singly_access_token']
        return kwargs

    def get(self, **kwargs):
        return super(Resource, self).get(**self._get_kwargs(kwargs))

    def post(self, **kwargs):
        return super(Resource, self).post(**self._get_kwargs(kwargs))


class Singly(ResourceAttributesMixin, slumber.API):
    """
    Wrapper over slumber.API which will automatically create resources
    which will automatically send access token to every request.

    First of all access token must be obtained by calling authenticate method.

    """

    def __init__(self, app_key, app_secret):
        super(Singly, self).__init__(API_BASE_URL, append_slash=False)
        self._store.update({
            'singly_key': app_key,
            'singly_secret': app_secret,
        })

    def authenticate(self, code):
        """
        Try to authenticate with returned code
        This code must be obtained from a callback url to wich
        a user will be redirected after successfull authentication

        """
        params = {
            'client_id': self._store['singly_key'],
            'client_secret': self._store['singly_secret'],
            'code': code
        }

        logger.debug("Trying to get access token with this params %s" % (params,))
        response = self.oauth.access_token.get(**params)
        logger.debug("Access token response data is %s" % (response, ))

        # Expect
        # {
        # "access_token": "S0meAcc3ssT0k3n"
        # }
        access_token = response.get('access_token')
        logger.debug("Access token is %s" % (access_token, ))
        self._store['singly_access_token'] = access_token
        return access_token
