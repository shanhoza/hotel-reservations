import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "email,exists",
    [
        ("test@test.com", True),
        ("artem@example.com", True),
        ("...", False),
    ],
)
async def test_find_user_by_email(email, exists):
    user = await UserDAO.find_one_or_none(email=email)

    if exists:
        assert user
        assert user["email"] == email
    else:
        assert not user
