from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review

def index(request):
    q = request.GET.get('q','').strip()
    movies = Movie.objects.all()
    if q:
        movies = movies.filter(title__icontains=q)
    return render(request, 'movies/index.html', {
        'template_data': {'title':'Movies', 'movies': movies, 'q': q}
    })

def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = movie.reviews.order_by('-created_at')
    return render(request, 'movies/show.html', {
        'template_data': {'title': movie.title, 'movie': movie, 'reviews': reviews}
    })

@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        comment = request.POST.get('comment','').strip()
        if comment:
            Review.objects.create(movie=movie, user=request.user, comment=comment)
    return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    movie = get_object_or_404(Movie, id=id)
    review = get_object_or_404(Review, id=review_id, movie=movie)
    if review.user != request.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        return render(request, 'movies/edit_review.html', {
            'template_data': {'title':'Edit Review', 'review': review, 'movie': movie}
        })
    comment = request.POST.get('comment','').strip()
    if comment:
        review.comment = comment
        review.save()
    return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    movie = get_object_or_404(Movie, id=id)
    review = get_object_or_404(Review, id=review_id, movie=movie)
    if review.user == request.user:
        review.delete()
    return redirect('movies.show', id=id)
