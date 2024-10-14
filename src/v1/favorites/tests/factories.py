import factory
from faker import Factory as FakerFactory

from v1.customers.tests.factories import CustomerFactory
from v1.favorites.models import FavoriteProduct, Product

faker = FakerFactory.create()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    id = factory.Faker("pyint", min_value=100000, max_value=999999)
    title = factory.Faker("sentence", nb_words=3)
    image = factory.Faker("image_url")
    price = factory.Faker("pyfloat", left_digits=5, right_digits=2, positive=True)
    review_score = factory.Faker("pyint", min_value=1, max_value=5)


class FavoriteProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoriteProduct

    favorite = factory.LazyAttribute(lambda _: CustomerFactory().favorite)
    product = factory.SubFactory(ProductFactory)
