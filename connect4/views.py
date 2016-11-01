from django.shortcuts import render, redirect, render_to_response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
import models
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
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
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(request.GET.get('next',
                                        settings.LOGIN_REDIRECT_URL))
        else:
            return HttpResponse('Invalid. Please try again ')
    args = {}
    args.update(csrf(request))
    username = password = ''
    args['form'] = AuthenticationForm()
    return render_to_response('login.html', args, context_instance=RequestContext(request))

def logout(request):
    """
    write your logout view here
    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect('/connect4/login/')

def signup(request):
    """
    write your user sign up view here
    :param request:
    :return:
    """
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponse('Sucessfully Signed Up')
        username = request.POST.get('username');
        password = request.POST.get('password1')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponseRedirect('/connect4/login/')
    else:
        # return HttpResponse('Username already exists or password does not match')
        form = UserCreationForm()
        args['form'] = form
    return render_to_response('signup.html', args, context_instance=RequestContext(request))


@login_required(login_url='/connect4/login/')
def games(request):
    """
    Write your view which controls the game set up and selection screen here
    :param request:
    :return:
    """
    # creating game
    if request.method == 'POST':
        player1 = request.user
        game = Game(player1=player1)
        game.save()
    args = {}
    args.update(csrf(request))

    args['allMyCreatedGames'] = Game.objects.all().filter(status='Open', player1=request.user)
    args['allOpenGames'] = Game.objects.all().filter(status='Open').exclude(player1=request.user)
    args['allPlayingGames'] = Game.objects.all().filter(Q(status='Playing'),
                                                        Q(player1=request.user) | Q(player2=request.user))
    args['allConcludedGames'] = Game.objects.all().filter(Q(status='Concluded'),
                                                          Q(player1=request.user) | Q(player2=request.user))
    return render_to_response('game.html', args, context_instance=RequestContext(request))


@login_required(login_url='/connect4/login/')
def play(request, game_id):
    """
    write your view which controls the gameplay interaction w the web layer here
    :param request, game_id:
    :return:
    """
    game = Game.objects.get(id=game_id)
    if game.player1 != request.user:
        game.join_up(request.user)
    if request.method == 'POST':
        if game.status == 'Concluded':
            return HttpResponseBadRequest('Game already finished!')
        elif game.status == 'Playing' and request.user.id not in [game.player1_id, game.player2_id]:
            return HttpResponseBadRequest("Only current players are allowed to make the move")
        elif not game.coin_set.all() or game.last_move.player != request.user:
            status = request.POST.get('status', 'Open')
            row = request.POST.get('row')
            col = request.POST.get('column')
            game.make_move(request.user, row, col)
            if status == 'Concluded':
                game.status = 'Concluded'
                game.winner = request.user.username
                game.save()
        else:
            return HttpResponseBadRequest("Can not make 2 moves in a row")
    args = {}
    args.update(csrf(request))
    args['game'] = game
    args['coin_set'] = game.coin_set
    args['player_turns'] = [coin.player_id for coin in game.coin_set.all()]
    args['rows'] = [coin.row for coin in game.coin_set.all()]
    args['cols'] = [coin.column for coin in game.coin_set.all()]
    args['last_move'] = game.last_move if len(game.coin_set.all()) else None
    return render_to_response('play.html', args, context_instance=RequestContext(request))
