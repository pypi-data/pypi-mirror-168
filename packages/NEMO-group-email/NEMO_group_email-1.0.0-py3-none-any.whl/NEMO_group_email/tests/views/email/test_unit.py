from unittest.mock import Mock

from NEMO.models import User
from django.contrib.auth.models import Group
from django.test import TestCase

from NEMO_group_email.views.email import new_get_users_for_email


class TestNewGetUsersForEmail(TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup fixtures for the tests"""
        super().setUpClass()

        cls.group1 = Group.objects.create(name="group1")
        cls.group2 = Group.objects.create(name="group2")
        cls.group3 = Group.objects.create(name="group3")

        cls.user1 = User.objects.create(
            username="user1", first_name="Testy", last_name="McTester"
        )
        cls.user1.groups.add(cls.group1)
        cls.user1.groups.add(cls.group2)
        cls.user2 = User.objects.create(
            username="user2", first_name="Testy", last_name="McTester"
        )
        cls.user2.groups.add(cls.group2)
        cls.user2.groups.add(cls.group3)
        cls.user3 = User.objects.create(
            username="user3", first_name="Testy", last_name="McTester"
        )
        cls.user3.groups.add(cls.group3)

    def setUp(self) -> None:
        """Setup unwrap the function for better control."""
        self.new_get_users_for_email = new_get_users_for_email.__wrapped__

    def test_non_group_audience_returns_old_function(
        self,
    ):
        expected_results = "mock_old_function"
        mock_replace_function = Mock()
        mock_replace_function.return_value = expected_results

        results = self.new_get_users_for_email(
            mock_replace_function, "non_group", None, True
        )

        self.assertEqual(results, expected_results)

    def test_single_group(self):
        query = [f"{self.group2.pk}"]
        expected_results = [self.user1, self.user2]

        results = self.new_get_users_for_email(None, "group", query, True)

        self.assertEqual(list(results), expected_results)

    def test_single_and_group(self):
        query = [f"{self.group1.pk} {self.group2.pk}"]
        expected_results = [self.user1]

        results = self.new_get_users_for_email(None, "group", query, True)

        self.assertEqual(list(results), expected_results)

    def test_complex_queries(self):
        query_list = [
            [f"{self.group1.pk} {self.group2.pk}", f"{self.group2.pk}"],
            [f"3 {self.group1.pk}"],
            [
                f"{self.group1.pk} {self.group2.pk}",
                f"{self.group3.pk} {self.group1.pk}",
            ],
            [
                f"{self.group1.pk} {self.group2.pk}",
                f"{self.group3.pk}",
                f"{self.group2.pk} {self.group3.pk}",
            ],
            [f"{self.group1.pk}", f"{self.group1.pk}"],
            [f"{self.group1.pk}", f"{self.group2.pk}", f"{self.group3.pk}"],
        ]
        expected_results_list = [
            [self.user1, self.user2],
            [],
            [self.user1],
            [self.user1, self.user2, self.user3],
            [self.user1],
            [self.user1, self.user2, self.user3],
        ]

        for query_index, query in enumerate(query_list):
            results = self.new_get_users_for_email(None, "group", query, True)
            self.assertEqual(list(results), expected_results_list[query_index])
