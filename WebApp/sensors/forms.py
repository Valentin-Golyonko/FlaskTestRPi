from django import forms

from sensors.models import Sensors


class NewSensor(forms.ModelForm):
    class Meta:
        model = Sensors
        fields = '__all__'
