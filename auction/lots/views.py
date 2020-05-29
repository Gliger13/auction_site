from django.core.paginator import Paginator
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


def page(request, num):
    if request.method == 'GET':
        lots_list = Lot.objects.all()

        paginator = Paginator(lots_list, 5)



        page_number = num
        page_obj = paginator.get_page(page_number)
        print(page_obj)
        return render(
            request,
            'lots/page.html',
            context={
                'lots': page_obj
            }
        )
