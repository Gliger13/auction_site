from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone

from auction import settings
from lots import tags_of_images
from lots.forms import LotsForm, SetBitForm
from lots.models import Lot, Bet


@login_required
def create(request):
    if request.method == 'GET':
        form = LotsForm()
        return render(
            request,
            'lots/create.html',
            context={'form': form}
        )
    elif request.method == 'POST':
        lot = Lot()
        lot.author = request.user
        lot.set_price = 0
        form = LotsForm(request.POST, request.FILES, instance=lot)
        if form.is_valid():
            lot = form.save()
            lot.image = request.FILES['image']
            lot.save()
            async_tags = async_to_sync(tags_of_images.images_tags, force_new_loop=True)
            async_tags(lot)
            return redirect(f"/lots/lot/{lot.id}")
        else:
            return render(
                request,
                'lots/create.html',
                context={'form': form}
            )


def page(request, num):
    if request.method == 'GET':
        lots_list = Lot.objects.all()

        paginator = Paginator(lots_list, settings.PAGINATOR_MAX_PAGES, orphans=2)
        page_number = num
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'lots/page.html',
            context={
                'lots': page_obj
            }
        )


def lot(request, lot_id):
    lot = Lot.objects.filter(id=lot_id).get()
    expires_at_str = str(lot.expires_at).replace(' ', 'T')
    is_POST_request = False
    if request.method == 'GET':
        form = SetBitForm()
        return render(
            request,
            'lots/lot.html',
            context={
                'lot': lot,
                'expires_at_str': expires_at_str,
                'is_POST_request': is_POST_request,
                'form': form
            }
        )
    elif request.method == 'POST':
        is_POST_request = True
        if request.user:
            bet = Bet.objects.filter(lot=lot, set_by=request.user)
            if not bet.exists():
                bet = Bet()
                bet.lot = lot
                bet.set_by = request.user
            else:
                bet = bet.get()
            form = SetBitForm(request.POST, instance=bet)

            if (form.is_valid() and
                    form.clean_lot(lot)
                    and lot.expires_at > timezone.now()):
                form.is_correct = True
                form.save()
                return render(
                    request,
                    'lots/lot.html',
                    context={
                        'lot': lot,
                        'expires_at_str': expires_at_str,
                        'is_POST_request': is_POST_request,
                        'form': form
                    }
                )
            else:
                form.is_correct = False
                return render(
                    request,
                    'lots/lot.html',
                    context={
                        'lot': lot,
                        'form': form,
                        'expires_at_str': expires_at_str,
                        'is_POST_request': is_POST_request,
                    })
        else:
            return redirect('account/login')
