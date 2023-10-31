from .forms import LoginForm, ProfileEditForm, ProfileForm, UserEditForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from cards.models import CreditCard
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.profile.status == 'AC':
                    login(request, user)
                    return redirect('dashboard')
                elif user.profile.status == 'DO':
                    return HttpResponse('Your account is inactive, please check your email to reactivate it')
                else:
                    return HttpResponse('Account is blocked')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})



@login_required
def dashboard(request):
    credit_cards = CreditCard.objects.filter(user=request.user)
    print(credit_cards)
    return render(request, 'account/dashboard.html', {'credit_cards': credit_cards})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            
            # Obtener el último código
            last_profile = Profile.objects.order_by('-code').first()
            if last_profile:
                last_code = last_profile.code
                last_num = int(last_code.split('-')[1])
                new_num = last_num + 1
                new_code = f"A2-{new_num:04d}"
            else:
                new_code = "A2-0001"
            
            # Create the user profile
            Profile.objects.create(user=new_user, code=new_code)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'account/register.html', {'user_form': user_form,'profile_form': profile_form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form}
    )

@login_required
def deactivate_account(request):
    # Obtener el usuario actual
    user = request.user

    # Cambiar el estado del usuario a 'Inactivo'
    user.profile.status = 'DO'  # Asegúrate de reemplazar 'User' por tu modelo de usuario si es diferente

    # Generar un token de reactivación
    reactivation_token = get_random_string(length=32)
    user.profile.reactivation_token = reactivation_token

    # Guardar los cambios en la base de datos
    user.profile.save()

    # Enviar el correo de reactivación
    subject = 'Reactivate Your Account'
    message = f'Click the link to reactivate your account: http://localhost:8000/account/reactivate/{reactivation_token}'
    from_email = 'your_email@example.com'
    to_list = [user.email]

    send_mail(subject, message, from_email, to_list, fail_silently=True)

    # Cerrar la sesión del usuario
    logout(request)

    # Redirigir al usuario a la página de inicio
    return redirect('dashboard')

def reactivate_account(request, token):
    # Buscar un usuario con el token de reactivación proporcionado
    user = get_object_or_404(User, profile__reactivation_token=token)

    # Cambiar el estado del usuario a 'Activo'
    user.profile.status = 'AC'  # Asegúrate de reemplazar 'User' por tu modelo de usuario si es diferente

    # Eliminar el token de reactivación
    user.profile.reactivation_token = None

    # Guardar los cambios en la base de datos
    user.profile.save()

    # Iniciar sesión del usuario
    login(request, user)

    # Redirigir al usuario a la página de inicio
    return redirect('dashboard')
