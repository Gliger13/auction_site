from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

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
        form = LotsForm(request.POST, request.FILES)
        if form.is_valid():
            lot = form.save()
            lot.image = request.FILES['image']
            lot.save()
            return redirect("/")
        else:
            return render(
                request,
                'lots/create.html',
                context={'form': form}
            )


def page(request, num):
    if request.method == 'GET':
        lots_list = Lot.objects.all()

        paginator = Paginator(lots_list, 5, orphans=2)

        page_number = num
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'lots/page.html',
            context={
                'lots': page_obj
            }
        )


@login_required
def lot(request, lot_id):
    lot = Lot.objects.filter(id=lot_id).get()
    if request.method == 'GET':
        form = SetBitForm()
        return render(
            request,
            'lots/lot.html',
            context={
                'lot': lot,
                'form': form
            }
        )
    elif request.method == 'POST':
        bet = Bet()
        bet.lot = lot
        form = SetBitForm(request.POST, instance=bet)
        if form.is_valid() and form.clean_lot(lot):
            form.is_correct = True
            form.save()
            return render(
                request,
                'lots/lot.html',
                context={
                    'lot': lot,
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
                    'form': form
                })
