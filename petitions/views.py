from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Petition, PetitionVote


def index(request):
    petitions = Petition.objects.annotate(
        yes_count=Count('votes', filter=Q(votes__yes=True))
    ).select_related('created_by').order_by('-created_at')
    return render(request, 'petitions/index.html', {
        'template_data': {'title': 'Petitions'},
        'petitions': petitions,
    })


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'petitions/create.html', {
            'template_data': {'title': 'New Petition'}
        })
    title = (request.POST.get('title') or '').strip()
    desc = (request.POST.get('description') or '').strip()
    if title:
        Petition.objects.create(title=title, description=desc, created_by=request.user)
        return redirect('petitions.index')
    return render(request, 'petitions/create.html', {
        'template_data': {'title': 'New Petition'},
        'error': 'Title is required.'
    })


@login_required
def vote_yes(request, id):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=id)
        PetitionVote.objects.get_or_create(petition=petition, user=request.user, defaults={'yes': True})
    return redirect('petitions.index')


