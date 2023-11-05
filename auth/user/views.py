from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Donation, ChildrenOrphanage, User, Review, Visit
import jwt, datetime, secrets
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.decorators import user_passes_test
from .forms import EditOrphanageForm, AddOrphanageForm, AddUserForm, VisitForm, ReviewForm, DonationForm

# Create your views here.
#Authentications.
def is_chief(user):
    return user.role == 'Chief'

def is_user(user):
    return user.role == 'User'

class registerView(APIView):
  def post(self, request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
  
class loginView(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()
    if user is None:
      raise AuthenticationFailed('user not found!')
    
    if not user.check_password(password):
      raise AuthenticationFailed('incorrect password!')
    
    payload ={
      'id':user.id,
      'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }
    # token = jwt.encode(payload, 'secret', algorithm= 'HS256').decode('utf-8')
    token_bytes = jwt.encode(payload, 'secret', algorithm='HS256')
    refresh_token = secrets.token_urlsafe(20)

    if isinstance(token_bytes, bytes):
        token = token_bytes.decode('utf-8')
    else:   
        token = token_bytes

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {'jwt': token, 'refresh_token': refresh_token}

    if user.role == 'Chief':
        return HttpResponseRedirect(reverse('chief_dashboard'))  # Use 'reverse' with the URL name
    elif user.role == 'User':
        return HttpResponseRedirect(reverse('home'))  # Use 'reverse' with the URL name
    else:
        raise AuthenticationFailed('Invalid user role')
    # return response
  
class userView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('Not authenticated')
    
    try:
      payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Token expired or invalid')
    
    user = User.objects.filter(id =payload['id']).first()

    if user.role == 'Chief':
        return HttpResponseRedirect(reverse('chief_dashboard'))  # Use 'reverse' with the URL name
    elif user.role == 'User':
        return HttpResponseRedirect(reverse('home'))  # Use 'reverse' with the URL name
    else:
        raise AuthenticationFailed('Invalid user role')
   

class logoutView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data ={
      'message': 'delete successful'
    }
    return response
  
def home(request):
  return render(request, 'default/home.html')

def about(request):
  return render(request, 'default/about.html')

def contact(request):
  return render(request, 'default/contact.html')

@login_required
# @user_passes_test(is_user)
def reviews(request): 
    review = Review.objects.all()
    return render(request, 'default/children_homes.html', {'review': review})

@login_required
# @user_passes_test(is_chief)
def visit(request):
    visit = Visit.objects.all()
    context = {
        "visit": visit,
    }
    return render(request, 'default/visit.html', context)

@login_required
# @user_passes_test(is_chief)
def children_orphanages(request):
    homes = ChildrenOrphanage.objects.all()
    context = {
        "homes": homes,
    }
    return render(request, 'default/children_homes.html', context)

@login_required
# @user_passes_test(is_user)
def donations(request):
    donations = Donation.objects.all()
    context = {
        'donations': donations,
    }
    return render(request, 'default/donations.html', context)
@login_required
# @user_passes_test(is_chief)
def orphanage_search(request):
    if 'query' in request.GET:
        query = request.GET['query']
    else:
        query = None

    if 'location' in request.GET:
        location = request.GET['location']
    else:
        location = None

    if query and location:
        results = ChildrenOrphanage.objects.filter(name__icontains=query, location__icontains=location)
    elif query:
        results = ChildrenOrphanage.objects.filter(name__icontains=query)
    elif location:
        results = ChildrenOrphanage.objects.filter(location__icontains=location)
    else:
        results = None

    return render(request, 'default/children_homes_search.html', {'results': results})

@login_required
# @user_passes_test(is_user)
def orphanage_detail(request, id):
    children_home = ChildrenOrphanage.objects.get(id=id)
    return render(request, 'default/children_home_detail.html', {'children_home': children_home})

#Adding functionality in user 
@login_required
@user_passes_test(is_user)
def make_donations(request, id):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            children_home = ChildrenOrphanage.objects.get(id=id)

            # Update needs based on the type of donation made
            if donation.donated_item == 'clothes':
                ChildrenOrphanage.objects.filter(id=id).update(needs_clothes=F('needs_clothes') - 1)
            elif donation.donated_item == 'hygiene':
                ChildrenOrphanage.objects.filter(id=id).update(needs_hygiene_supplies=F('needs_hygiene_supplies') - 1)
            elif donation.donated_item == 'food':
                ChildrenOrphanage.objects.filter(id=id).update(needs_food=F('needs_food') - 1)
            elif donation.donated_item == 'money':
                ChildrenOrphanage.objects.filter(id=id).update(needs_money=F('needs_money') - 1)

            donation.children_orphanage = children_home
            donation.save()
            return redirect('donations')
    else:
        form = DonationForm()
    return render(request, 'user/donation_form.html', {'form': form})

@login_required
@user_passes_test(is_user)
def schedule_visit(request, id):
    user_visits = Visit.objects.filter(user=request.user, visit_date__gte=timezone.now())
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            home = ChildrenOrphanage.objects.get(id=id)
            visit.children_orphanage = home
            visit.save()

            # Increment the visit count for the home
            home.visit += 1
            home.save()

            return redirect('events')
    else:
        form = VisitForm()
    return render(request, 'user/visit_form.html', {'form': form, 'user_visits':user_visits})

@login_required
@user_passes_test(is_user)
def submit_review(request, id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.children_orphanage = ChildrenOrphanage.objects.get(id=id)
            review.save()
            return redirect('reviews')
    else:
        form = ReviewForm()

    return render(request, 'user/submit_review.html', {'form': form})

#Admin MVP
@login_required
@user_passes_test(is_chief)
def chief_dashboard(request):
    return render(request, 'chief/dashboard.html')

#User CRUD
@login_required
@user_passes_test(is_chief)
def all_users(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'chief/all_users.html', context)

@login_required
@user_passes_test(is_chief)
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = AddUserForm()

    return render(request, 'chief/add_user.html', {'form': form})

#Children Home CRUD
@login_required
@user_passes_test(is_chief)
def add_orphanage(request):
    if request.method == 'POST':
        form = AddOrphanageForm(request.POST, request.FILES)
        if form.is_valid():
            new_home = form.save(commit=False)
            new_home.save()
            return redirect('children_homes', id=new_home.id)
    else:
        form = AddOrphanageForm()
    return render(request, 'chief/add_home.html', {'form': form})

@login_required
@user_passes_test(is_chief)
def edit_orphanage(request, id):
    if request.method == 'POST':
        home = ChildrenOrphanage.objects.get(id=id)
        form = EditOrphanageForm(request.POST, instance=home)
        if form.is_valid:
            form.save()
            return redirect('children_home_detail')
    else:
        home = ChildrenOrphanage.objects.get(id=id)
        form = EditOrphanageForm(instance=home)
    return render(request, 'chief/homes.html', {'form': form})

@login_required
@user_passes_test(is_chief)
def delete_orphanage(request, id):
    home = ChildrenOrphanage.objects.get(id=id)
    if request.method == 'POST':
        home.delete()
        return redirect('chief_dashboard')

    context = {'home': home}
    return render(request, 'chief/delete_home.html', context)

#Analytics
@login_required
@user_passes_test(is_chief)
def most_visited_home(request):
    upcoming_visits = Visit.objects.filter(visit_date__gte=timezone.now())
    most_visited_home = ChildrenOrphanage.objects.order_by('-visit').first()
    context = {'most_visited_home': most_visited_home, "upcoming_visits": upcoming_visits}
    return render(request, 'chief/most_visited_home.html', context)

@login_required
@user_passes_test(is_chief)
def most_in_need_home(request):
    most_in_need_home = ChildrenOrphanage.objects.order_by('-needs').first()
    context = {'most_in_need_home': most_in_need_home}
    return render(request, 'chief/most_in_need_home.html', context)