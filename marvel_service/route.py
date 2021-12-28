"""Module route keeps endpoints
   and provide poor functional to handle those
"""


def create_route(url_mapping):

    bounded_urls = URLsBinding()
    for method in url_mapping:
        func_name = eval(f"bounded_urls.bind_{method}")
        [func_name(*i) for i in url_mapping[method]]

    return bounded_urls


class URLsBinding:
    """Class which allow bind functions to the URL"""

    def __init__(self):
        self._bind_end_points: dict = {}

    def show_end_points(self):
        print(self._bind_end_points)

    def binding(self,  method: str, url: str, function) -> None:
        """
        Creates structure dictionary of dictionaries to the self.bind_end_points
        self._bind_end_points : {
            'url': {
                'get': <function_n>,
                'post': <function_n1>
                'delete': <function_n2>
                'patch': <function_n3>
            }
        }
        :param method: get, post, patch, delete
        :param url: end point
        :param function: function object
        :return: None
        """
        pair_method_function = {method: function}
        if url in self._bind_end_points:
            self._bind_end_points[url].update(pair_method_function)
        else:
            self._bind_end_points[url] = pair_method_function

    def bind_get(self, url: str, func) -> None:
        self.binding("get", url, func)

    def bind_post(self, url: str, func) -> None:
        self.binding("post", url, func)

    def bind_delete(self, url: str, func) -> None:
        self.binding("delete", url, func)

    def bind_patch(self, url: str, func) -> None:
        self.binding("patch", url, func)

    def _func(self, url: str, method: str):
        """ _func - returns link on object function tied with url and method"""
        return self._bind_end_points[url][method]

    def endpoint_exists(self, endpoint) -> bool:
        exists = False
        if endpoint in self._bind_end_points:
            exists = True

        return exists

    def bound_get_and_func(self, url: str):
        return self._func(url, "get")

    def bound_post_and_func(self, url: str):
        return self._func(url, "post")

    def bound_delete_and_func(self, url: str):
        return self._func(url, "delete")

    def bound_patch_and_func(self, url: str):
        return self._func(url, "patch")


class EndPoints:
    """Class for handling end-points"""

    def __init__(self):
        self._end_points: dict = {}

    def add_endpoint(self, end_point: str, methods=["GET", "POST"]):
        """add name of endpoint

           By default, methods GET and POST are available to use with added
           endpoint
        """

        self._end_points[end_point] = methods

    def valid_endpoint(self, end_point_to_validate: str) -> bool:
        """Endpoint exists or not"""

        is_valid = False

        if end_point_to_validate in self._end_points.keys():
            is_valid = True

        return is_valid

    def change_available_methods(self, end_point: str,
                                 methods: [str] = ('GET', 'POST')
                                 ) -> bool:
        """change_available_methods - method gives ability to set up available
           REST methods

           REST API methods in a list - it tells items in a list are
           available methods to aplay to the URI
           Can be added rest methods : GET, POST, PATCH, DELETE
        """
        available_methods = {'get', 'post', 'delete', 'patch'}
        assign_methods = [i.upper() for i in methods if i.lower() in
                          available_methods]

        if self.valid_endpoint(end_point) and len(assign_methods) > 0:
            self._end_points[end_point] = assign_methods
            return True

        return False

    def endpoint_methods(self, end_point: str) -> [str]:
        """endpoint_methods - function return name of REST API methods which
        allows to aplay to the URI
        end_point: string - name of end point
        return: list of methods, will return empty list:
                - if methods not exists
                - if URI not exists or not valid
        """
        methods = []
        if self.valid_endpoint(end_point):
            methods.extend(self._end_points[end_point])

        return methods

    @property
    def endpoints(self) -> list:
        """return: list of all endpoints"""

        return list(self._end_points.keys())


if __name__ == "__main__":
    pass
