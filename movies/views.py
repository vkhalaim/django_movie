from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies_list.html'


class MovieDetailView(DetailView):

    model = Movie
    slug_field = 'url'
