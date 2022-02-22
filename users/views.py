from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.


def register(request):
    if request.method == 'POST':
        # POST request/ submitting details from the form.
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()  # Create the details if user is valid
            username = request.POST['username']
            # showing success message if user created successfully
            messages.success(request, f'{username} is Created Successfully!!!')
            return redirect('login')  # redirect to login page

    else:
        form = UserRegisterForm()  # for gettting the page/ GET request

    return render(request, template_name='register.html', context={'form': form})
