from django.shortcuts import render
from django.http import HttpResponse

from . import util

import markdown as md

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def CSS(request):
    return render(request, "encyclopedia/CSS.html", {
        "css_content": md.markdown(util.get_entry("CSS"))
    })

def wiki(request):
    return render(request, "encyclopedia/wiki.html")


def content(request, title):
        return render(request, "encyclopedia/content.html", {
            "html_content": md.markdown(util.get_entry(title))
        })

def fourofour(request, exception=None):
    return render(request, "encyclopedia/fourofour.html")