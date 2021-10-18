from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect


def login_view(request):
    """
    Render login view
    @param request:
    @return:
    """
    form = AuthenticationForm(request, data=request.POST or None)

    if form.is_valid():
        login(request, form.get_user())
        return redirect('/')

    context = {
        "form": form
    }

    return render(request, "accounts/login.html", context=context)


def logout_view(request):
    """
    Render logout view
    @param request:
    @return:
    """

    context = {}

    if request.method == "POST":
        logout(request)
        return redirect("/login/")

    return render(request, "accounts/logout.html", context=context)


def register_view(request):
    """
    Render register view
    @param request:
    @return:
    """

    # Check if there is the request.POST,
    # else it is None, and make the form is not valid
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context=context)
