import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

import src.app as app_module


class TeacherAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.credentials_file = Path(self.temp_dir.name) / "teachers.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_teachers(self):
        self.credentials_file.write_text(
            json.dumps({"teachers": [{"username": "coach", "password": "test-pass"}]}),
            encoding="utf-8",
        )

    def test_valid_teacher_is_authenticated(self):
        self.write_teachers()
        credentials = HTTPBasicCredentials(username="coach", password="test-pass")

        with patch.object(app_module, "teachers_file", self.credentials_file):
            self.assertEqual(app_module.require_teacher(credentials), "coach")

    def test_invalid_password_is_rejected(self):
        self.write_teachers()
        credentials = HTTPBasicCredentials(username="coach", password="wrong")

        with patch.object(app_module, "teachers_file", self.credentials_file):
            with self.assertRaises(HTTPException) as error:
                app_module.require_teacher(credentials)

        self.assertEqual(error.exception.status_code, 401)

    def test_missing_credentials_are_rejected(self):
        with self.assertRaises(HTTPException) as error:
            app_module.require_teacher(None)

        self.assertEqual(error.exception.status_code, 401)

    def test_activity_list_is_public(self):
        route = next(route for route in app_module.app.routes
                     if getattr(route, "path", None) == "/activities")

        self.assertEqual(route.dependant.dependencies, [])

    def test_signup_and_unregister_require_teacher(self):
        expected_paths = {
            "/activities/{activity_name}/signup",
            "/activities/{activity_name}/unregister",
        }
        protected_routes = [route for route in app_module.app.routes
                            if getattr(route, "path", None) in expected_paths]

        self.assertEqual(len(protected_routes), 2)
        for route in protected_routes:
            self.assertIn(
                app_module.require_teacher,
                [dependency.call for dependency in route.dependant.dependencies],
            )


if __name__ == "__main__":
    unittest.main()