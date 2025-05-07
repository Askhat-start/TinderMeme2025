from django.shortcuts import render
from . import models
from django.db.models import Subquery
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Count, Q


def getUnswipedMemes(user):
    swiped_memes = models.Swipe.objects.filter(user=user).values('meme')
    memes = models.Meme.objects.exclude(id__in=Subquery(swiped_memes))[:10]
    return memes


def main(request):
    if request.user.is_authenticated:
        memes = getUnswipedMemes(request.user)
    else:
        memes = models.Meme.objects.all()

    return render(request, 'main/base.html', context={'memes': memes, 'request': request})


@csrf_exempt
def swipe_meme(request):
    if request.method == "POST":
        data = json.loads(request.body)
        meme_id = data.get('meme_id')
        action = data.get('action')

        meme = models.Meme.objects.get(id=meme_id)
        swipe, created = models.Swipe.objects.get_or_create(
            user=request.user,
            meme=meme,
            defaults={'action': action}
        )

        if not created:
            swipe.action = action
            swipe.save()

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@login_required
def save_meme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        meme_id = data.get('meme_id')

        print(f"HERE IS YOUR FUCKING MEME ID: {meme_id}")
        print(f"JSON SHIT {data}")

        meme = models.Meme.objects.get(id=meme_id)

        _, created = models.SavedMemes.objects.get_or_create(
            user=request.user,
            meme=meme
        )

        return JsonResponse({'status': 'saved' if created else 'already_saved'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def show_saved(request):
    if request.user.is_authenticated:
        saved = models.SavedMemes.objects.filter(user=request.user).values_list("meme", flat=True)
        saved_memes = models.Meme.objects.filter(id__in=saved)
        return render(request, 'main/main.html', context={'saved_memes': saved_memes})


def calculate_user_matches(user):
    liked_memes = models.Swipe.objects.filter(user=user, action='like').values_list('meme_id', flat=True)

    if liked_memes.count() < 10:
        return []

    matches = (
        models.Swipe.objects
        .filter(meme_id__in=liked_memes, action='like')
        .exclude(user=user)
        .values('user')
        .annotate(similarity_score=Count('meme'))
        .order_by('-similarity_score')
    )

    for match in matches:
        matched_user = models.User.objects.get(id=match['user'])
        models.Matches.objects.update_or_create(
            user=user,
            matched_with=matched_user,
            defaults={'similarity_score': match['similarity_score']}
        )

    return matches


@login_required
def show_matches(request):
    calculate_user_matches(request.user)
    matches = models.Matches.objects.filter(user=request.user).select_related('matched_with').order_by('-similarity_score')
    return render(request, 'main/matches.html', context={'matches': matches})
