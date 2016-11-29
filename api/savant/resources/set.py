from rest_framework import serializers, viewsets

from savant.api.savant.models import Set


class SetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Set
        fields = '__all__'


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
