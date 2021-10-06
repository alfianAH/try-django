"""
To render HTML web page
"""

from django.http import HttpResponse


def home_view(request):
    """
    Make home view
    @param request: Django's request
    @return: Returns HTML as a response
    """

    name = "Alfian"
    html_string = """
    <h1>Hello {}</h1>
    """.format(name)

    return HttpResponse(html_string)
