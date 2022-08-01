from rest_framework import serializers, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet
from django.contrib.auth import get_user_model
from core.models import Quote
from core.services.services import create_quote

User = get_user_model()


class QuotesViewSet(ViewSet, CreateModelMixin):
    queryset = Quote.objects.none()
    permission_classes = [IsAuthenticated]

    class InputModelSerializer(serializers.ModelSerializer):
        had_previously_cancel_volcano_policy = serializers.BooleanField(default=False)
        never_cancel_volcano_policy = serializers.BooleanField(default=False)
        new_property = serializers.BooleanField(default=False)
        address = serializers.CharField(
            default="1600 Pennsylvania Avenue NW, Washington, DC 20500"
        )

        class Meta:
            model = Quote
            fields = (
                "had_previously_cancel_volcano_policy",
                "never_cancel_volcano_policy",
                "new_property",
                "address",
                "effective_date",
                "policy_holder",
            )

    def create(self, request, *args, **kwargs):
        serializer = self.InputModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_quote(
            effective_date=serializer.data["effective_date"],
            had_previously_cancel_volcano_policy=serializer.data[
                "had_previously_cancel_volcano_policy"
            ],
            never_cancel_volcano_policy=serializer.data["never_cancel_volcano_policy"],
            new_property=serializer.data["new_property"],
            address=serializer.data["address"],
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.none()
    permission_classes = [IsAuthenticated]

    class UserSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = User
            fields = ["url", "username", "email"]

    def get_serializer_class(self):
        return self.UserSerializer
