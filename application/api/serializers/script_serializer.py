from rest_framework import serializers

from application.models import Script

class ScriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Script
        fields = '__all__'
