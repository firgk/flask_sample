import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SecuritySourceTest(unittest.TestCase):
    def test_auth_does_not_trust_legacy_cookie(self):
        source = (ROOT / "tools" / "auth.py").read_text(encoding="utf-8")
        self.assertNotIn('request.cookies.get("logged_in")', source)
        self.assertIn('session.get("logged_in")', source)
        self.assertIn('session["logged_in"] = True', source)

    def test_password_is_not_hardcoded(self):
        source = (ROOT / "tools" / "auth.py").read_text(encoding="utf-8")
        self.assertNotIn('LOGIN_PASSWORD = "123456"', source)
        self.assertIn('os.environ.get("LOGIN_PASSWORD")', source)
        self.assertIn('raise RuntimeError("LOGIN_PASSWORD environment variable is required")', source)

    def test_debug_is_disabled(self):
        source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("debug=True", source)
        self.assertIn("debug=False", source)
        self.assertIn("SESSION_COOKIE_HTTPONLY=True", source)
        self.assertIn('SESSION_COOKIE_SAMESITE="Lax"', source)


if __name__ == "__main__":
    unittest.main()
