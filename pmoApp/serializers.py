from django.shortcuts import render
from rest_framework import serializers
from pmoApp.models import justificationReport,authorizationReport


class JustificationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = justificationReport
        fields = '__all__'

class AuthorizationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = authorizationReport
        fields = '__all__'