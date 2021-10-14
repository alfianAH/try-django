from django.contrib.auth import authenticate, login, logout
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

    context = {}
    return render(request, "accounts/register.html", context=context)