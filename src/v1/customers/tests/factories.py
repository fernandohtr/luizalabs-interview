import factory
from faker import Factory as FakerFactory

from v1.customers.models import Customer

faker = FakerFactory.create()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda x: faker.first_name())
    email = factory.LazyAttribute(lambda x: faker.email())


class CustomerWithProductsFactory(CustomerFactory):
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
