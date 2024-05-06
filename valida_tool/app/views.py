from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound

from .models import Validation, Answer, Participation, Item

import random


# Create your views here.

@login_required(login_url='/accounts/login/')
def index(request):
    error = request.session.get('current_error', None)
    if error:
        del request.session['current_error']
    return render(request, 'dashboard.html', {
        "validations": request.user.validation_set.all(),
        "error": error,
        "total_messages": Item.objects.count(),
        "messages_validated": Answer.get_validated_num(),
        "messages_user_validated": len(Answer.objects.filter(user_id=request.user.id))
    })


@login_required(login_url='/accounts/login/')
def guide(request, validation_id):
    return render(request, 'guide.html', {
        "validation": Validation.objects.get(pk=validation_id)
    })


@login_required(login_url='/accounts/login/')
def validation(request, validation_id):
    # Check if user really is participating in the validation and get current item
    current_participation = Participation.objects.filter(user_id=request.user.id, validation_id=validation_id)
    if len(current_participation) == 0:
        return HttpResponseNotFound()
    elif len(current_participation) > 1:
        return HttpResponse(status=500)
    current_participation = current_participation[0]
    current_validation = Validation.objects.get(pk=validation_id)

    # Deal with the response from the form
    if request.method == "POST":
        if current_participation.current_item is None:
            return HttpResponse(status=500)
        data = dict(request.POST)
        del data['csrfmiddlewaretoken']
        answer = Answer(user=request.user, item=current_participation.current_item, validation=current_validation,
                        answer_data=data)
        answer.save()
        current_participation.current_item = None
        current_participation.save()
        request.session['current_error'] = "Your answer was sent. " \
                                           "Thanks for participating!"
        return redirect(index)

    # Prepare the right item for user.
    if current_participation.current_item is None:
        list_items = {}
        has_neuro = {}
        participation_objs = Participation.objects.filter(validation_id=current_validation.id)
        for participation in participation_objs:
            if participation.current_item is not None:
                # Get ids of users participating in this item
                if participation.current_item.id not in list_items:
                    list_items[participation.current_item.id] = []
                if participation.current_item.id not in has_neuro:
                    has_neuro[participation.current_item.id] = False
                list_items[participation.current_item_id].append(participation.user.id)
                # Check if a neuro user is already participating
                if participation.user.groups.filter(name="Neuro").exists():
                    has_neuro[participation.current_item.id] = True
        answer_objs = Answer.objects.filter(validation_id=current_validation.id)
        for answer in answer_objs:
            if answer.item_id not in list_items:
                list_items[answer.item_id] = []
            if answer.item_id not in has_neuro:
                has_neuro[answer.item_id] = False
            list_items[answer.item_id].append(answer.user.id)
            if answer.user.groups.filter(name="Neuro").exists():
                has_neuro[answer.item_id] = True

        current_user_is_neuro = request.user.groups.filter(name="Neuro").exists()
        max_allowed = current_validation.answers_per_item

        for item_id, users_associated in list_items.items():
            if len(users_associated) >= max_allowed:
                continue
            elif len(users_associated) < max_allowed:
                if has_neuro[item_id] and current_user_is_neuro:
                    continue
                if not has_neuro[item_id] and not current_user_is_neuro and len(users_associated) == max_allowed - 1:
                    continue
                # User may have a previous answer for this item
                if request.user.id in users_associated:
                    continue
                current_participation.current_item = Item.objects.get(pk=item_id)
                current_participation.save()
                break

        # If it is still none after the loop attribute a random item
        if current_participation.current_item is None:
            remaining_items = Item.objects.exclude(id__in=list_items.keys())
            if len(remaining_items) == 0:
                request.session['current_error'] = "No more items are available for this validation. " \
                                                   "Thanks for participating!"
                return redirect(index)
            current_participation.current_item = random.sample(list(remaining_items), 1)[0]
            current_participation.save()

    return render(request, 'validations/{}.html'.format(validation_id), {
        "validation": Validation.objects.get(pk=validation_id),
        "payload": dict(current_participation.current_item.payload),
    })