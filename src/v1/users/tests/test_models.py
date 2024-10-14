import pytest
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@pytest.mark.django_db
def test_create_normal_user(normal_user):
    assert normal_user.username is not None
    assert normal_user.email is not None
    assert normal_user.password is not None
    assert normal_user.is_active
    assert not normal_user.is_staff
    assert not normal_user.is_superuser


@pytest.mark.django_db
def test_create_super_user(super_user):
    assert super_user.username is not None
    assert super_user.email is not None
    assert super_user.password is not None
    assert super_user.is_active
    assert super_user.is_staff
    assert super_user.is_superuser


@pytest.mark.django_db
def test_update_user(normal_user):
    new_username = "John"
    normal_user.username = new_username
    normal_user.save()
    updated_user = CustomUser.objects.get(pk=normal_user.pk)

    assert updated_user.username == new_username


@pytest.mark.django_db
def test_delete_user(normal_user):
    user_pk = normal_user.pk
    normal_user.delete()

    with pytest.raises(CustomUser.DoesNotExist):
        CustomUser.objects.get(pk=user_pk)


@pytest.mark.django_db
def test_user_str(normal_user):
    assert str(normal_user) == normal_user.email


@pytest.mark.django_db
def test_normal_user_email_is_normalized(normal_user):
    email = normal_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_super_user_email_is_superized(super_user):
    email = super_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_user_email_incorrect(custom_user_factory):
    with pytest.raises(ValueError) as error:  # noqa: PT011
        custom_user_factory.create(email="failmail.com")
    assert str(error.value) == "You must provide a valid email address."


@pytest.mark.django_db
def test_create_user_with_no_email(custom_user_factory):
    with pytest.raises(ValueError) as error:  # noqa: PT011
        custom_user_factory.create(email=None)
    assert str(error.value) == "User must have an email address."


@pytest.mark.django_db
def test_create_superuser_with_no_email(custom_user_factory):
    with pytest.raises(ValueError) as error:  # noqa: PT011
        custom_user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(error.value) == "Superuser must have an email address."


@pytest.mark.django_db
def test_create_superuser_with_no_password(custom_user_factory):
    with pytest.raises(ValueError) as error:  # noqa: PT011
        custom_user_factory.create(password=None, is_superuser=True, is_staff=True)
    assert str(error.value) == "Superuser must have a password."


@pytest.mark.django_db
def test_create_superuser_is_not_staff(custom_user_factory):
    with pytest.raises(ValueError) as error:  # noqa: PT011
        custom_user_factory.create(is_superuser=True, is_staff=False)
    assert str(error.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_create_superuser_is_not_superuser(custom_user_factory):
    with pytest.raises(ValueError) as error:  # noqa: PT011
        custom_user_factory.create(is_superuser=False, is_staff=True)
    assert str(error.value) == "Superuser must have is_superuser=True."
