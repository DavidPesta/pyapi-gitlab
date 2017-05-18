import os
from unittest import TestCase

import responses

from gitlab import Gitlab
from gitlab.exceptions import HttpError
from gitlab_tests.base import BaseTest
from response_data.users import *


class TestGetUsers(BaseTest):
    @responses.activate
    def test_get_users(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/users',
            match_querystring=False,
            json=get_users,
            status=200,
            content_type='application/json')

        self.assertEqual(get_users, self.gitlab.get_users())
        self.assertEqual(get_users, self.gitlab.get_users(search='test'))
        self.assertEqual(get_users, self.gitlab.getusers())

    @responses.activate
    def test_get_users_exception(self):
        responses.add(
            responses.GET,
            self.gitlab.api_url + '/users',
            match_querystring=False,
            json='{"error": "Not found"}',
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.get_users)
        self.assertEqual(False, self.gitlab.getusers())


class TestDeleteUser(BaseTest):
    @responses.activate
    def test_delete_user(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/users/14',
            json=delete_user,
            status=204,
            content_type='application/json')

        self.assertEqual(delete_user, self.gitlab.delete_user(14))
        self.assertTrue(self.gitlab.deleteuser(14))

    @responses.activate
    def test_get_users_exception(self):
        responses.add(
            responses.DELETE,
            self.gitlab.api_url + '/users/14',
            body='{"error": "Not found"}',
            status=404,
            content_type='application/json')

        self.assertRaises(HttpError, self.gitlab.delete_user, 14)
        self.assertFalse(self.gitlab.deleteuser(14))
