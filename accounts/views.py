from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def login_view(request):
    """
    Render login view
    @param request:
    @return:
    """

    context = {}

    if request.method == "POST":
        post_dict = request.POST

        # Get input form
        username = post_dict.get("username")
        password = post_dict.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            context["error"] = "Invalid username or password"
            return render(request, "accounts/login.html", context=context)

        login(request, user)
        return redirect('/')
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
