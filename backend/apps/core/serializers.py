from rest_framework import serializers


class CustomMultipleChoiceField(serializers.MultipleChoiceField):
    def to_representation(self, value):
        return {self.choices[item] for item in value}
