from django import forms

from lots.models import Lot, Bet


class LotsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.lot = None
        super(LotsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) == forms.Textarea:
                visible.field.widget.attrs['class'] = 'uk-textarea input-form'
            else:
                visible.field.widget.attrs['class'] = 'uk-input input-form'

    text_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 3,
        })
    )

    tags = forms.CharField(
        label="Tags. Separate tags by ';'",
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 3,
        })
    )

    base_price = forms.IntegerField(
        widget=forms.NumberInput(),
        required=True,
    )
    image = forms.FileField(
        widget=forms.FileInput
    )

    class Meta:
        model = Lot
        fields = [
            'heading',
            'text_description',
            'tags',
            'base_price',
            'min_price_step',

        ]

    def is_valid(self):
        return super(LotsForm, self).is_valid()

    def save(self, commit=True):
        self.instance.current_price = self.cleaned_data.get('base_price')
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
                int(self.data['set_price']) - lot.current_price < lot.min_price_step or
                lot.base_price >= int(self.data['set_price'])):
            return False
        else:
            lot.current_price = int(self.data['set_price'])
            lot.save()
            return True


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) == forms.Select:
                visible.field.widget.attrs['class'] = 'uk-select'
            else:
                visible.field.widget.attrs['class'] = 'uk-input'

    CHOICES = [
        ('price_lth', 'Price: Low to High'),
        ('price_htl', 'Price: High to Low'),
        ('created_lth', 'Created: High to Low'),
        ('created_htl', 'Created: Low to High'),
        ('time_left_lth', 'Time left: High to Low'),
        ('time_left_htl', 'Time left: Low to High'),
    ]

    min_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
    )

    max_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
    )

    by_author = forms.CharField(
        widget=forms.TextInput,
        required=False,
    )

    order_by = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select,
        required=False,
    )

    class Meta:
        fields = [
            'min_price',
            'max_price',
            'by_author',
            'order_by',
        ]
