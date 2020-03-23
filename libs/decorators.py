# -*- coding:utf-8 -*-


import functools
import urllib
from tornado.web import HTTPError
from tornado.options import options


class route(object):
    """
    usage:

    @route('/apply-async/(.*)/')
    class ApplyAsyncHandler(ApplyHandlerBase):
    def post(self, taskname):
        print(taskname)
    """
    _routes = []

    def __init__(self, regexp):
        self._regexp = regexp

    def __call__(self, handler):
        """gets called when we class decorate"""
        self._routes.append((self._regexp, handler))
        return handler

    @classmethod
    def get_routes(cls):
        return cls._routes

def require(role):
    def req_decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.current_user is None:
                raise HTTPError(403)
            if self.is_role(role):
                return method(self, *args, **kwargs)
            else:
                raise HTTPError(403)
        return wrapper

    return req_decorator

def admin(method):
    """Decorate with this method to restrict to site admins."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method == "GET":
                url = self.get_login_url()
                if "?" not in url:
                    url += "?" + urllib.urlencode(dict(next=self.request.full_url()))
                self.redirect(url)
                return
            raise HTTPError(403)
        elif not self.is_admin:
            if self.request.method == "GET":
                self.redirect(options.home_url)
                return
            raise HTTPError(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper


def staff(method):
    """Decorate with this method to restrict to site staff."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method == "GET":
                url = self.get_login_url()
                if "?" not in url:
                    url += "?" + urllib.urlencode(dict(next=self.request.full_url()))
                self.redirect(url)
                return
            raise HTTPError(403)
        elif not self.is_staff:
            if self.request.method == "GET":
                self.redirect(options.home_url)
                return
            raise HTTPError(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper


def authenticated(role):
    """Decorate methods with this to require that the user be logged in.
    
    Fix the redirect url with full_url. 
    Tornado use uri by default.
    
    """
    def _wrapper(method):
        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            if self.current_user is None:
                raise HTTPError(403)
            return await method(self, *args, **kwargs)
        return wrapper
    return _wrapper()
