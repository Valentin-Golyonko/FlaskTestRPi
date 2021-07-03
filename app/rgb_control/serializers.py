from rest_framework import serializers


class SendColorSerializer(serializers.Serializer):
    red = serializers.IntegerField(required=True, min_value=0, max_value=255)
    green = serializers.IntegerField(required=True, min_value=0, max_value=255)
    blue = serializers.IntegerField(required=True, min_value=0, max_value=255)
    alpha = serializers.FloatField(required=True, min_value=0, max_value=1)
