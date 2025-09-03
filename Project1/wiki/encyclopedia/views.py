from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect

from . import util

import markdown as md

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#page de test
def CSS(request):
    return render(request, "encyclopedia/CSS.html", {
        "css_content": md.markdown(util.get_entry("CSS"))
    })

def wiki(request):
    return render(request, "encyclopedia/wiki.html")

def content(request, title):
        try:
            return render(request, "encyclopedia/content.html", {
                "html_content": md.markdown(util.get_entry(title))
            })
        except(AttributeError):
             raise Http404("Page not found.")

def custom_404_view(request, exception):
    return render(request, 'encyclopedia/404.html', status=404)

def search_result(request):
    user_search = request.GET.get('q')
    if util.get_entry(user_search):
         return redirect(content, title=user_search)
    else:
        return render(request, "encyclopedia/search_result.html", {
            "user_search": user_search,
            "results": util.search_results(user_search)
        })
    
def new_page(request):
    return render(request, "encyclopedia/new_page.html")