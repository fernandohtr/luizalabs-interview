import factory
from django.contrib.auth import get_user_model
from faker import Factory as FakerFactory

faker = FakerFactory.create()
CustomUser = get_user_model()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    name = factory.LazyAttribute(lambda x: faker.first_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)

        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class CustomUserWithProductsFactory(CustomUserFactory):
    @factory.post_generation
    def favorite(self, create, extracted, **kwargs):
        if not create:
            return

        from v1.favorites.tests.factories import ProductFactory

        if extracted:
            for product in extracted:
                self.favorite.products.add(product)
        else:
            for _ in range(5):
                product = ProductFactory()
                self.favorite.products.add(product)
