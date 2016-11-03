from django.shortcuts import render, redirect, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
import models
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django import forms
from app import settings
from models import Game
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages


# Create your views here.
def login(request):
    """
    Write your login view here
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/connect4/games/')
    else:
        form = AuthenticationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('login.html', args)


def logout(request):
    """
    write your logout view here
    :param request:
    :return:
    """
    auth.logout(request)
    return redirect(login)


def signup(request):
    """
    write your user sign up view here
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/connect4/login/')
    else:
        form = UserCreationForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('signup.html', args)


# @login_required(login_url='/connect4/login/')
def games(request):
    """
    Write your view which controls the game set up and selection screen here
    :param request:
    :return:
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/connect4/login/')
    else:
        # creating game
        if request.method == 'POST':
            player1 = request.user
            game = Game(player1=player1)
            game.save()

        my_created_games = Game.objects.all().filter(status='Open', player1=request.user)
        open_games = Game.objects.all().filter(status='Open').exclude(player1=request.user)
        playing_games = Game.objects.all().filter(Q(status='Playing'),
                                                  Q(player1=request.user) | Q(player2=request.user))
        concluded_games = Game.objects.all().filter(Q(status='Concluded'),
                                                    Q(player1=request.user) | Q(player2=request.user))
        context = {'my_created_games': my_created_games,
                   'open_games': open_games,
                   'playing_games': playing_games,
                   'concluded_games': concluded_games}
        return render(request, 'game.html', context)


# @login_required(login_url='/connect4/login/')
def play(request, game_id):
    """
    write your view which controls the gameplay interaction w the web layer here
    :param request, game_id:
    :return:
    """
    game = Game.objects.get(id=game_id)
    if game.player1 != request.user:
        game.join_up(request.user)

    coin_set = game.coin_set
    player_turns = [coin.player_id for coin in game.coin_set.all()]
    rows = [coin.row for coin in game.coin_set.all()]
    cols = [coin.column for coin in game.coin_set.all()]
    last_move = game.last_move if len(game.coin_set.all()) else None
    context = {
        'game': game,
        'coin_set': coin_set,
        'player_turns': player_turns,
        'rows': rows,
        'cols': cols,
        'last_move': last_move
    }
    return render(request, 'play.html', context)
