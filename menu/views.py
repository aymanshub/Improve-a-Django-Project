from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def sorter(a):
    """
    a method acts as key sorter for sorted python method
    orders objects by expiration_date ascending
    """
    if not a.expiration_date:
        return date.min
    return a.expiration_date


def menu_list(request):
    """
    view method for getting, sorting and rendering unexpired menu seasons.
    """
    menus = Menu.objects.prefetch_related('items').exclude(expiration_date__lt=date.today())
    menus = sorted(menus, key=sorter)
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    """
    view method for menu details, including food items
    """
    try:
        menu = Menu.objects.prefetch_related('items').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """
    view method for item details
    """
    try:
        item = Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


@login_required
def create_new_menu(request):
    """
    view method for creating and saving new menu
    """
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            menu.items.set(form.cleaned_data['items'])
            messages.add_message(request, messages.SUCCESS, menu.season + ' menu has been successfully added.')
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm(initial={'created_date': date.today})
    return render(request, 'menu/menu_new.html', {'form': form})


@login_required
def edit_menu(request, pk):
    """
    view method for editing an existing menu
    if no change has occurred during edit, the db wont be hit
    """
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            if form.has_changed():
                menu = form.save()
                menu.items.set(form.cleaned_data['items'])
                messages.add_message(request, messages.INFO, menu.season + ' has been successfully updated.')
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form})


@login_required
def delete_menu(request, pk):
    """
    view method for deleting existing menu
    """
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu.delete()
        messages.add_message(request, messages.INFO, menu.season + ' menu has been successfully removed.')
        return HttpResponseRedirect(reverse('menu_list'))
    else:
        form = DeleteForm(initial={'season': menu.season})
        return render(request, 'menu/menu_delete.html', {'form': form})

