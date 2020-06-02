from django.contrib import admin

from lots.models import Lot, Bet, ImageTags

admin.site.register(Lot)
admin.site.register(Bet)
admin.site.register(ImageTags)
