from app.tests.client import APITestClient
from typing import List
from pydantic import parse_obj_as
from app.dto.user import User


class Test_DatalakeControllerSpec():

    @classmethod
    def setup_class(cls):
        cls.test_client: APITestClient = APITestClient()

    @classmethod
    def teardown_class(cls):
        cls.test_client.__del__()

    def test_get_users(self):
        response = self.test_client.client \
            .get("/datawarehouse/users/")
        assert response.status_code == 200

        user_data = parse_obj_as(List[User], response.json())
        assert len(user_data) == 2
