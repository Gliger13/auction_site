from django import forms

from lots.models import Lot, Bet


class LotsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LotsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input input-form'

    text_description = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
    base_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=True
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


class SetBitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SetBitForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input uk-form-width-medium'

    set_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=True
    )

    class Meta:
        model = Bet
        fields = [
            'set_price'
        ]

    def is_valid(self):
        return super(SetBitForm, self).is_valid()

    def clean_lot(self, lot):
        if (lot.current_price >= int(self.data['set_price']) or
                lot.base_price >= int(self.data['set_price'])):
            return False
        else:
            lot.current_price = int(self.data['set_price'])
            lot.save()
            return True