import factory
from faker import Factory as FakerFactory

from v1.favorites.models import Favorite, FavoriteProduct, Product
from v1.users.tests.factories import CustomUserFactory

faker = FakerFactory.create()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    id = factory.Faker("pyint", min_value=100000, max_value=999999)
    title = factory.Faker("sentence", nb_words=3)
    image = factory.Faker("image_url")
    price = factory.Faker("pyfloat", left_digits=5, right_digits=2, positive=True)
    review_score = factory.Faker("pyint", min_value=1, max_value=5)


class FavoriteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    user = factory.SubFactory(CustomUserFactory)


class FavoriteWithProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Favorite

    user = factory.SubFactory(CustomUserFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.add(product)
        else:
            for _ in range(5):
                product = ProductFactory()
                self.products.add(product)


class FavoriteProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoriteProduct

    favorite = factory.SubFactory(FavoriteWithProductFactory)
    product = factory.SubFactory(ProductFactory)
