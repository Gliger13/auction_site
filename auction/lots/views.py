from django.shortcuts import render, redirect

from lots.forms import LotsForm
from lots.models import Lot


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

def page(request):
    user = request.user
    lots = Lot.objects.all()
    for lot in lots:
        a = lot.image

    if request.method == 'GET':
        return render(
            request,
            'lots/page.html',
            context={
                'lots': lots
            }
        )
