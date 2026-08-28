import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from django.shortcuts import render
from .models import Movie


def home(request):
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(
        request,
        'home.html',
        {
            'searchTerm': searchTerm,
            'movies': movies
        }
    )


def about(request):
    return render(request, 'about.html')


def statistics_view(request):
    matplotlib.use('Agg')

    # ==================================================
    # GRÁFICA 1: PELÍCULAS POR AÑO
    # ==================================================

    years = Movie.objects.values_list(
        'year',
        flat=True
    ).distinct().order_by('year')

    movie_counts_by_year = {}

    for year in years:

        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.bar(
        bar_positions,
        movie_counts_by_year.values(),
        width=bar_width,
        align='center'
    )

    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')

    plt.xticks(
        bar_positions,
        movie_counts_by_year.keys(),
        rotation=90
    )

    plt.subplots_adjust(bottom=0.3)

    # Guardar la gráfica en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la gráfica a Base64
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')


    # ==================================================
    # GRÁFICA 2: PELÍCULAS POR GÉNERO
    # Se considera únicamente el primer género
    # ==================================================

    genres = Movie.objects.values_list(
        'genre',
        flat=True
    )

    movie_counts_by_genre = {}

    for genre in genres:

        if genre:
            first_genre = genre.split(',')[0].strip()
        else:
            first_genre = "None"

        if first_genre in movie_counts_by_genre:
            movie_counts_by_genre[first_genre] += 1
        else:
            movie_counts_by_genre[first_genre] = 1

    genre_positions = range(len(movie_counts_by_genre))

    plt.bar(
        genre_positions,
        movie_counts_by_genre.values(),
        width=bar_width,
        align='center',
        color='purple'
    )

    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')

    plt.xticks(
        genre_positions,
        movie_counts_by_genre.keys(),
        rotation=90
    )

    plt.subplots_adjust(bottom=0.3)

    # Guardar segunda gráfica en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir segunda gráfica a Base64
    image_png = buffer.getvalue()
    buffer.close()

    graphic_genre = base64.b64encode(image_png)
    graphic_genre = graphic_genre.decode('utf-8')


    # Enviar las dos gráficas a statistics.html
    return render(
        request,
        'statistics.html',
        {
            'graphic': graphic,
            'graphic_genre': graphic_genre
        }
    )

def signup(request):
    email = request.GET.get('email')

    return render(
        request,
        'signup.html',
        {
            'email': email
        }
    )