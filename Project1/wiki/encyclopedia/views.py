from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages 

from . import util

import markdown as md

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    return render(request, "encyclopedia/wiki.html")

def content(request, title):
    '''Affiche le contenu en HTML d'une entrée du wiki'''
    try:
        return render(request, "encyclopedia/content.html", {
            "html_content": md.markdown(util.get_entry(title)),
            "title":title
        })
    except(AttributeError):
            raise Http404("Page not found.")

def custom_404_view(request):
    return render(request, 'encyclopedia/404.html', status=404)

def search_result(request):
    '''Affiche toutes les entrées contenant le string requête user'''
    user_search = request.GET.get('q')
    if util.get_entry(user_search):
         return redirect(content, title=user_search)
    else:
        return render(request, "encyclopedia/search_result.html", {
            "user_search": user_search,
            "results": util.search_results(user_search)
        })
    
def new_page(request):
    '''Créer une nouvelle page avec le titre du md est le titre du fichier'''
    try:
        if(request.GET.get("bouton_add")):
            title = request.GET.get('title')
            util.create_new_page(title, request.GET.get('content'))
            return redirect(content, title=title)
        else: 
            return render(request,'encyclopedia/new_page.html')
    except(FileExistsError):
        print("Fichier déjà existant")
        return render(request, "encyclopedia/new_page.html", {
            "error_page_already_exists" : "A page with the same name already exists"
        })
    
def edit_page(request, title):
    '''Edit la page du contexte en annule/remplace. Permet aussi de renommer le fichier'''
    try:
        if(request.GET.get("bouton_edit")):
            util.edit_page(title, request.GET.get('new_title'), request.GET.get('new_content'))
            return redirect(content, title=title)
        else:
            return render(request, "encyclopedia/edit_page.html", {
                        "html_content": (util.get_entry(title)),
                        "title":title
                    })
    except(FileExistsError):
        return render(request, "encyclopedia/edit_page.html", {
            "error_page_already_exists" : "A page with the same name already exists"
        })
    
def random_page(request):
    '''Retourne 1 valeur de la liste des entrées du wiki'''
    try:
        random_title = util.get_random_page()
        print(random_title)
        return redirect(content, title=random_title)
    except(AttributeError):
            raise Http404("Page not found.")