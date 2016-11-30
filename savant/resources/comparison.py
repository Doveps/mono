from rest_framework import serializers, viewsets

from savant.models import Comparison


class ComparisonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comparison
        fields = '__all__'


class ComparisonViewSet(viewsets.ModelViewSet):
    queryset = Comparison.objects.all()
    serializer_class = ComparisonSerializer
