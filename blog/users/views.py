from django.shortcuts import render, redirect
from .forms import UserCreationCustomForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationCustomForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            username = form.cleaned_data['username']
            return redirect('home')
    else:
        form = UserCreationCustomForm()
    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid() and p_form.is_valid():
            username = u_form.cleaned_data['username']
            messages.success(request, f" Yo {username}, your profile has been updated!!!!")
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'users/profile.html', context)


