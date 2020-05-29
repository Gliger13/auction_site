from django import forms

from lots.models import Lot


class LotsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LotsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input-form'

    text_description = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
    base_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=False
    )
    image = forms.FileField()

    class Meta:
        model = Lot
        fields = [
            'heading',
            'text_description',
            'base_price',
        ]

    def is_valid(self):
        return super(LotsForm, self).is_valid()

    def save(self, commit=True):
        return super().save(commit)
