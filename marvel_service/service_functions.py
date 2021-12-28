"""
   Module contain functions and urlmapping structure

   functions - will be bind with endpoints, have to be filled out with
   custom code to work with data

   urlmapping - dict of tuples
   keys: - name of REASTP API methods
   values - tuple of pairs where first item is url second item in pair is
   function name


"""

import re
import json
from .route import create_route
from .data_storage import HeroesTableHandler, heroes
from .data_storage import squads, Group, calculate_power

heroes_table = HeroesTableHandler(heroes)
squad_table = Group(squads)


def heroes_get(*args, **kwargs):
    heroes_dict = {"heroes": []}
    try:
        heroes_dict["heroes"] = heroes_table.get_all_heroes()
    finally:
        return json.dumps(heroes_dict)


def hero_get(name):
    """Get info about hero"""
    hero_info = {}

    try:
        result_lst = heroes_table.get_hero_info(name)

        if len(result_lst) == 0:
            hero_info = ""
        else:
            hero_info[name] = result_lst
    finally:
        return json.dumps(hero_info)


def heroes_delete(entity):
    heroes_table.delete_hero(entity)
    squad_table.delete_hero_from_squads(entity)

def heroes_post(body: dict):
    for k, v in body.items():
        name = k
        lst_body = v

    if not heroes_table.add_entity(name, lst_body):
        raise AttributeError
    else:
        return True


def heroes_patch(entity, body):
    # we interested to update only good and alive status
    if not heroes_table.validate_hero(entity):
        return

    if body['alive']:
        if body['alive'] == 'dead':
            heroes_table.make_dead(entity)
        elif body['alive'] == "alive":
            heroes_table.make_alive(entity)
        else:
            heroes_table.make_injured(entity)

    if body['good']:
        if body['good'] is True:
            heroes_table.set_good(entity)
        else:
            heroes_table.set_good(entity, False)


def squad_get(name):
    "Info squad"
    squad_info = {}

    try:
        result_lst = squad_table.get_squad_info(name)

        if len(result_lst) == 0:
            squad_info = ""
        else:
            squad_info[name] = result_lst
    finally:
        return json.dumps(squad_info)


def squads_get(*args, **kwargs):
    squad_dict = {"squads": []}
    try:
        squad_dict["squads"] = squad_table.get_all_squads()
    finally:
        return json.dumps(squad_dict)


def squad_delete(entity):
    squad_table.delete_squad(entity)


def squad_post(body: dict):
    for k, v in body.items():
        name = k
        lst_body = v

    if not squad_table.create_squad(name, lst_body,
                                    heroes_table.get_all_heroes()):
        raise AttributeError
    else:
        return True


def tournament(body: dict):
    answer = prepare_answer("Bad format, expected {'squad1': 'group', "
                            "'squad2': 'group''}", 422, False)
    if 'squad1' in body:
        group_name1 = body['squad1']
    else:
        return answer

    if 'squad2' in body:
        group_name2 = body['squad2']
    else:
        return answer

    if not squad_table.is_valid_squad(group_name1):
        return prepare_answer(f"Not Found {group_name1}"  , 404, False)

    if not squad_table.is_valid_squad(group_name2):
        return prepare_answer(f"Not Found {group_name2}"  , 404, False)

    result = calculate_power(heroes_table.heroes, squad_table.squads, group_name1,
                             group_name2)
    return prepare_answer(f"{result}"  , 200, True)


urlmapping = {
    'get': (('/heroes', heroes_get), ('/squads', squads_get),
            ('/heroes/{entity}', hero_get),
            ('/squads/{entity}', squad_get)),
    'delete': (('/heroes/{entity}', heroes_delete),
               ('/squads/{entity}', squad_delete)),
    'patch': (('/heroes/{entity}', heroes_patch),),
    'post': (('/heroes', heroes_post), ('/tournament', tournament), ('/squads', squad_post))
}


def prepare_answer(message, error_code: int, status: bool = True) -> dict:
    answer = {'status': status,
              'error_code': error_code,
              'message': message
              }
    return answer


class MethodsCallDispatcher:

    def _add_mapping(self, mapping):
        self.mapping = mapping

    def _init_route(self):
        self.route = create_route(self.mapping)
        return self.route

    def route_config(self, mapping):
        self._add_mapping(mapping)
        self._init_route()

    def on_get(self, url_path):

        pattern_with_entity = re.compile("^(/.+)/(.+)")
        pattern_endpoint = re.compile("^(/.+)$")
        pattern_with3section = re.compile("^(/.+)/(.+)/(.+)")
        # NOTE - it is on GET

        if pattern_with_entity.search(url_path.path) is not None:
            path_entity = pattern_with_entity.findall(url_path.path)[0]
            end_point, entity = path_entity

            if self.route.endpoint_exists(end_point):
                # extract function which bounded to current end_point
                function = \
                    self.route.bound_get_and_func(f"{end_point}/" + "{entity}")

                # executing of function bounded to the end-point, function
                # should return json

                json_result = function(entity)

                if json_result == '""':
                    answer = prepare_answer(f"Not Found {end_point}/{entity}",
                                            404, False)
                else:
                    answer = prepare_answer(json_result, 200, True)

                return answer
            else:
                answer = prepare_answer(f"Not Found: {end_point}", 404, False)

        elif pattern_endpoint.search(url_path.path):
            end_point = pattern_endpoint.findall(url_path.path)[0]
            if self.route.endpoint_exists(end_point):
                # extract function which bounded to current end_point
                function = self.route.bound_get_and_func(end_point)
                # executing of function bounded to the end-point, function
                # should return json
                json_result = function()
                answer = prepare_answer(json_result, 200, True)
            else:
                answer = prepare_answer(f"Not Found: {end_point}", 404, False)
        else:
            answer = prepare_answer(f"Bad Request: {url_path.path}", 400, False)

        return answer

    def _is_validate_post_json(self, body):
        answer = True
        try:
            json.loads(body)
        except:
            answer = False
        finally:
            return answer

    def on_post(self, url_path, body):

        if not self._is_validate_post_json(body):
            return prepare_answer("Check POST body", 422, False)

        body_dict = json.loads(body)
        answer = prepare_answer("", 201, True)
        pattern_end_point = re.compile("^(/.+)")

        if pattern_end_point.search(url_path.path) is not None:
            if self.route.endpoint_exists(url_path.path):
                # extract function which bounded to current end_point
                function = \
                    self.route.bound_post_and_func(url_path.path)

                try:
                    result_of_post = function(body_dict)

                    if type(result_of_post) is dict:
                        answer = result_of_post
                    else:
                        answer = prepare_answer("Created", 201, True)

                except AttributeError:
                    answer = prepare_answer("Check POST body", 422, False)

                finally:
                    return answer
            else:
                answer = prepare_answer(f"Not Found, endpoint: {url_path.path}",
                                        404, False)

        return prepare_answer(f"Bad Request: {url_path.path}", 400, False)

    def on_delete(self, url_path):
        pattern_with_entity = re.compile("^(/.+)/(.+)")
        # pattern_endpoint = re.compile("^(/.+)$")
        if pattern_with_entity.search(url_path.path) is not None:
            path_entity = pattern_with_entity.findall(url_path.path)[0]
            end_point, entity = path_entity

            if self.route.endpoint_exists(end_point):
                # extract function which bounded to current end_point
                function = \
                    self.route.bound_delete_and_func(
                        f"{end_point}/" + "{entity}"
                    )

                # executing of function bounded to the end-point, function
                # should return json
                function(entity)

                answer = prepare_answer("", 200, False)
            else:
                answer = prepare_answer(f"Not Found: {end_point}", 404, False)
        else:
            answer = prepare_answer(f"Bad Request: {url_path.path}", 400, False)

        return answer

    def on_patch(self, url_path, body):

        if not self._is_validate_post_json(body):
            return prepare_answer("Check PATCH body", 422, False)

        body_dict = json.loads(body)
        answer = prepare_answer("", 200, False)
        pattern_with_entity = re.compile("^(/.+)/(.+)")

        if pattern_with_entity.search(url_path.path) is not None:
            path_entity = pattern_with_entity.findall(url_path.path)[0]
            end_point, entity = path_entity

            if self.route.endpoint_exists(end_point):
                # extract function which bounded to current end_point
                function = \
                    self.route.bound_patch_and_func(f"{end_point}/" + "{"
                                                                      "entity}")
                try:
                    function(entity, body_dict)
                    answer = prepare_answer("Accepted", 202, True)
                except AttributeError:
                    answer = prepare_answer("Check PATCH body", 422, False)

                finally:
                    return answer
            else:
                answer = prepare_answer(f"Not Found, endpoint: {url_path.path}",
                                        404, False)

        return prepare_answer(f"Bad Request: {url_path.path}", 400, False)


if __name__ == "__main__":
    v = create_route(urlmapping)
    v.show_end_points()
    v1 = MethodsCallDispatcher()
    v1.route_config(urlmapping)
    v1.route.show_end_points()
