from django.shortcuts import render, redirect
from .forms import PostForm, PostForm2
from .models import Post, Bid
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta


def index(request):
    data = dict()
    data['title'] = 'My Lots'
    current_user = request.user
    data['posts'] = Post.objects.all().filter(user=current_user.id)
    return render(request, 'lots/index.html', context=data)

def create(request):
    data = dict()
    data['title'] = 'Add Lots'
    current_user = request.user
    if request.method == "GET":
        data['form'] = PostForm()
        print(data)
        return render(request, 'lots/create.html', context=data)
    elif request.method == 'POST':
        filled_form = PostForm(request.POST, request.FILES)
        fs = filled_form.save(commit=False)
        fs.user = current_user
        fs.save()
        time_left = fs.finish_date - fs.place_date
        print(time_left)
        return redirect('/lots')

def check(request, post_id):
    data = dict()
    data['title'] = 'Check Lots'
    tim = timezone.now()
    if request.method == "GET":
        auct = Post.objects.get(id=post_id)
        if auct.finish_date < tim + timedelta(seconds=301):
            prev_bid_price = Bid.objects.get(status='W', auct=auct)
            prev_bid_price.expire = 1
            prev_bid_price.save()
            auct.life_cycle = 'FN'
            auct.save()
            data['post'] = auct
            try:
                bi = Bid.objects.filter(status='W', auct=post_id, expire=1)
                if bi:
                    data['bigb'] = bi.get()
            except ObjectDoesNotExist:
                data['post'] = Post.objects.get(id=post_id)
            return render(request, 'lots/check.html', context=data)
        else:
            data['post'] = auct
            try:
                bi = Bid.objects.filter(status='W', auct=post_id, expire=1)
                if bi:
                    data['bigb'] = bi.get()
                else:
                    bi = Bid.objects.filter(status='W', auct=post_id, expire=0)
                    data['bigb'] = bi.get()
            except ObjectDoesNotExist:
                data['post'] = Post.objects.get(id=post_id)
            return render(request, 'lots/check.html', context=data)
    if request.user.is_authenticated:
        if request.method == 'POST':
            amount = request.POST['bid']
            try:
                float(amount)
            except:
                data['report_x'] = "You should input digits."
                return render(request, 'accounts/reports.html', context=data)
            auct = Post.objects.filter(id=post_id)
            if auct:
                auct = Post.objects.get(id=post_id)
                if auct.life_cycle == 'EX':
                    print("EXISTS")
                else:
                    data['report_x'] = "AUCTION IS OVER"
                    return render(request, 'accounts/reports.html', context=data)
            if auct.finish_date < tim:
                prev_bid_price = Bid.objects.get(status='W', auct=auct)
                prev_bid_price.expire = 1
                prev_bid_price.save()
                auct.life_cycle = 'FN'
                auct.save()
                data['report_x'] = "Sorry, Auction Is Over."
                return render(request, 'accounts/reports.html', context=data)
            if auct.min_price - float(amount) > 0:
                data['report_x'] = "You have to place bet higher or the same as starting price."
                return render(request, 'accounts/reports.html', context=data)
            prev_bid_wining = Bid.objects.filter(status='W', auct=auct)
            if prev_bid_wining:
                prev_bid_wining = Bid.objects.filter(status='W', auct=auct).get()
            if prev_bid_wining:
                if prev_bid_wining.user == request.user:
                    data['report_x'] = "You are already wining this auction."
                    return render(request, 'accounts/reports.html', context=data)
                if float(amount) - prev_bid_wining.amount < 1:
                    data['report_x'] = "Bid has to be at least bigger for 1$ than previous bids."
                    return render(request, 'accounts/reports.html', context=data)
                prev_bid_wining.status = 'L'
                prev_bid_wining.save()
            b = Bid(user=request.user, amount=float(amount), auct=auct, status='W')
            b.save()
            auct.finish_date += timedelta(minutes=5)
            auct.min_price = float(amount)
            auct.save()
            return redirect(f'/lots/check/{post_id}')
    else:
        return redirect('/accounts/sign_in')

def edit(request, post_id):
    data = dict()
    data['title'] = 'Edit lots'
    post = Post.objects.get(id=post_id)
    # del ... ?
    if request.method == 'GET':
        data['form'] = PostForm2(instance=post)
        data['post'] = post
        return render(request, 'lots/edit.html', context=data)
    elif request.method == 'POST':
        form2 = PostForm2(request.POST)
        if form2.is_valid():
            post.title = form2.cleaned_data['title']
            post.set = form2.cleaned_data['set']
            post.condition = form2.cleaned_data['condition']
            post.description = form2.cleaned_data['description']
            post.finish_date = form2.cleaned_data['finish_date']
            post.save()
            # update ?
        return redirect('/lots')

def remove(request, post_id):
    data = dict()
    data['title'] = 'Remove Lot'
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        data['post'] = post
        return render(request, 'lots/remove.html', context=data)
    elif request.method == 'POST':
        post.delete()
        return redirect('/lots')

def all_lots(request):
    data = dict()
    current_user = request.user
    data['title'] = 'All Lots'
    data['bigb'] = Bid.objects.all().exclude(expire=1)
    data['posts'] = Post.objects.all().exclude(user=current_user.id)
    return render(request, 'lots/all_lots.html', context=data)

def end_lot(request,post_id):
    tim = timezone.now()
    print('asss')
    if request.method == "GET":
        print('as2')
        auct = Post.objects.filter(id=post_id)
        auct_id = Bid.objects.filter(id=post_id)
        if auct:
            auct = Post.objects.get(id=post_id)
        if auct.finish_date < tim:
            auct_id.expire = 1
            print('GAME IS OVER')
        else:
            print('Not yet')
    else:
        return redirect('/lots')

def bid_lots(request):
    data = dict()
    current_user = request.user
    data['title'] = 'My Bids'
    # JOIN WITH MODE Bid by user
    data['posts'] = Post.objects.all().filter(bid__user_id=current_user.id)
    return render(request, 'lots/my_bids.html', context=data)
