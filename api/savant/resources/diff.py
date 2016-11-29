from rest_framework import serializers, viewsets

from savant.api.savant.models import Diff


class DiffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diff
        fields = '__all__'


class DiffViewSet(viewsets.ModelViewSet):
    queryset = Diff.objects.all()
    serializer_class = DiffSerializer
