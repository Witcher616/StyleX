from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from users.models import User, EmailVerification
from users.forms import UserLoginForm, UserRegistrForm, UserProfileForm
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from products.models import Basket
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'StyleX - Авторизация'
    }
    return render(request, 'users/login.html', context=context)


class UserRegistrView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы!'
    
    def get_context_data(self, **kwargs):
        context = super(UserRegistrView, self).get_context_data(**kwargs)
        context['title'] = 'StyleX - Регистрация'
        return context
    

# Ф-я для регистрации
'''def registr(request):
    if request.method == 'POST':
        form = UserRegistrForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)'''

class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id, ))   
    
    def get_context_data(self, **kwargs):
        baskets = Basket.objects.filter(user=self.object)
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['title'] = 'StyleX - Профиль'
        context['baskets'] = baskets
        context['total_quantity'] = sum(basket.quantity for basket in baskets)
        context['total_sum'] = sum([i.product.price * i.quantity for i in baskets])
        return context

#
'''@login_required
def profile(request):
    baskets = Basket.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    
    total_sum = 0
    total_quantity = 0
    
    for basket in baskets:
        total_sum += basket.sum()
        total_quantity += basket.quantity   
    
    context = {
        'title': 'Store-Профиль',
        'form': form,
        'baskets': baskets,
        'total_sum': total_sum,
        'total_quantity': total_quantity
    }
    return render(request, 'users/profile.html', context=context)'''

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

class EmailVerificationView(SuccessMessageMixin, TemplateView):
    title = 'Store - подверждение электронной почты'
    template_name = 'users/email_verification.html'
    
    def get(self, request, *args, **kwargs) -> HttpResponse:
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verify_email = True
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
