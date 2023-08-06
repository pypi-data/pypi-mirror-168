__version__ = "0.0.3"

import requests as _requests

_eureka_active = False
_eureka_available = None

def eureka_init(eureka_url):
    global _eureka_active, _eureka_available

    if not _eureka_active:
        try:
            from py_eureka_client.eureka_client import init as _eureka_init

            _eureka_init(
                eureka_url,
                should_register=False,
                app_name="eureka-requests"
            )

            _eureka_available = True
            _eureka_active = True
        except:
            _eureka_available = False
            print("No connection to the local server.")



class RequestsApi:

    def __init__(self, app, eureka_url, token="", extra_urls=[], verbose=False):
        r"""
        Encapsulate standard python requests 
        """
        self.__app = app

        self.__auth = ""
        if token != "":
            self.__auth = "bearer"
            self.__token = token

        self.__extra_urls = extra_urls
        self.__verbose = verbose

        eureka_init(eureka_url)

    def __check_url(self, url):
        if "http" in url:
            return "/".join(url.replace("http://", "").replace("https://", "").split("/")[1:])
        else:
            return url

    def _eureka_call(self, service, method, prefer_ip: bool = False, prefer_https: bool = False, **kwargs):
        """
        make an internal eureka service call
        """
        from py_eureka_client.eureka_client import get_client as _get_eureka_client

        # create a list of available service urls
        app_name = self.__app.upper()
        cli = _get_eureka_client()
        node = cli._EurekaClient__get_available_service(app_name)

        urls = []
        checked_nodes = []
        while node is not None:
            urls.append(cli._EurekaClient__generate_service_url(node, prefer_ip, prefer_https))
            checked_nodes.append(node.instanceId)
            node = cli._EurekaClient__get_available_service(app_name, checked_nodes)

        # add the extra_urls
        urls = [*urls, *self.__extra_urls]
        urls = list(set(urls))

        # order them by location
        ordered = False
        for loc in ["PEN", "WUX", "KLM", "RBG"]:
            if "/"+loc+"/" in service.upper():
                ordered = True
                urls = [
                    *[u for u in urls if loc in u.upper()], 
                    *[u for u in urls if loc not in u.upper()], 
                ]

        # if not ordered, search in RBG first (historically only rbg available)
        if not ordered:
            urls = [
                *[u for u in urls if "RBG" in u.upper()], 
                *[u for u in urls if "RBG" not in u.upper()], 
            ]

        if self.__verbose:
            print(f"Orderd urls for {service}: [{', '.join(urls)}]")            

        # loop the nodes an try to get a result
        for url in urls:
            try:
                if service.startswith("/"):
                    url = url + service[1:]
                else:
                    url = url + service

                if "timeout" not in kwargs:
                    kwargs["timeout"] = 1250

                res = getattr(_requests, method)(url=url, **kwargs)
                if self.__verbose:
                    print(f"Request with {url}")
                return res
            except Exception as ex:
                if self.__verbose:
                    print(f"Request failed with {url}")
                


    def __check_data(self, args):
        """
        add authentification to typical requests
        """
        if self.__auth == "bearer":
            if "headers" not in args:
                args["headers"] = {}
            args["headers"]["Authorization"] = f"Bearer {self.__token}"
        if self.__auth == "basic":
            args["auth"] = (self.__user, self.__password)

        return args

    def get(self, url, **kwargs):
        r"""Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="get")

    def options(self, url, **kwargs):
        r"""Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="options")

    def head(self, url, **kwargs):
        r"""Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="head")

    def post(self, url, **kwargs):
        r"""Sends a POST request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="post")

    def put(self, url, **kwargs):
        r"""Sends a PUT request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="put")

    def patch(self, url, **kwargs):
        r"""Sends a PATCH request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="patch")

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param **kwargs: Optional arguments that `request` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return self._eureka_call(self.__check_url(url), **self.__check_data(kwargs), method="delete")


