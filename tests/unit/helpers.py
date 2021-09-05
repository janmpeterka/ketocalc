from app.models.users import User


def create_user(username="test", password="testtest"):
    user = User(username=username)
    user.password = password
    user.set_password_hash(user.password.encode("utf-8"))
    user.first_name = "TEST"
    user.last_name = "TEST"
    user.password_version = "bcrypt"

    return user


def test_with_authenticated_user(app, username=None):
    @app.login_manager.request_loader
    def load_user_from_request(request, username=username):
        user = User.query.first() if not username else User.load_by_username(username)
        if user is None:
            assert False
        else:
            return user
