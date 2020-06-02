from lots.forms import FilterForm
from lots.models import Lot
from users.models import User


class LotsFilter:
    def __init__(self, form: FilterForm):
        self.form = form
        self.filter_by = dict()
        self.lots = None
        self.order_by = self.form.cleaned_data['order_by']

    def filtered_lots(self) -> [Lot]:
        self._by_price()
        self._by_author()
        self.lots = Lot.objects.filter(**self.filter_by)
        self._order()
        return self.lots

    def _by_author(self):
        if self.form.cleaned_data.get('by_author'):
            author = User.objects.filter(username=self.form.cleaned_data.get('by_author'))
            if author.exists():
                self.filter_by['author'] = author.get()
        else:
            print('error')

    def _by_price(self):

        if (self.form.cleaned_data.get('min_price') and
                self.form.cleaned_data.get('max_price')):

            self.filter_by['current_price__lte'] = self.form.cleaned_data.get('max_price')
            self.filter_by['current_price__gte'] = self.form.cleaned_data.get('min_price')
        elif self.form.cleaned_data.get('min_price'):
            self.filter_by['current_price__gte'] = self.form.cleaned_data.get('min_price')
        elif self.form.cleaned_data.get('max_price'):
            self.filter_by['current_price__lte'] = self.form.cleaned_data.get('max_price')
        else:
            print('error')

    def _order(self):
        if self.lots and self.order_by:
            if self.order_by == 'price_lth':
                self.lots = self.lots.order_by('current_price')
            elif self.order_by == 'price_htl':
                self.lots = self.lots.order_by('-current_price')
            elif self.order_by == 'created_lth':
                self.lots = self.lots.order_by('created_at')
            elif self.order_by == 'created_htl':
                self.lots = self.lots.order_by('-created_at')
            elif self.order_by == 'time_left_lth':
                self.lots = self.lots.order_by('expires_at')
            elif self.order_by == 'time_left_htl':
                self.lots = self.lots.order_by('-expires_at')
