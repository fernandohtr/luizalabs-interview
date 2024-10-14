from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from v1.customers.models import Customer
from v1.customers.serializers import CustomerSerializer


class CustomerListCreate(ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()


class CustomerRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()

    def get_object(self):
        email = self.request.query_params.get("email")
        if not email:
            raise NotFound(detail="Error: email query parameter is required")
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise NotFound(detail="Error: Customer with this email not found")
