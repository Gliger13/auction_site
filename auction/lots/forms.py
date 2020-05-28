from django import forms
from lots.models import Lots


class LotsForm(forms.ModelForm):
    class Meta:
        model = Lots
        fields = [
            'heading',
            'text_description',
            'base_price',
            'images',
        ]
 