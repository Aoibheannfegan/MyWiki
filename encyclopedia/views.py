from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
import markdown
from random import choice
from . import util


class NewPageForm(forms.Form):
    new_title = forms.CharField(label="Title")
    new_content = forms.CharField(widget=forms.Textarea, label = "Content")

class Edit(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='Edit Text')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    original_entry = util.get_entry(title)
    if original_entry:
        entry=markdown.markdown(original_entry)
        return render(request, "encyclopedia/page.html", {
            "entry": entry,
            "title":title.capitalize()
        })
    else:
         return render(request, "encyclopedia/error.html", {
            "title":title
        })
    
def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]
    if len(results) == 1 and results[0].lower() == query.lower():
        print(results)
        return render(request, "encyclopedia/page.html", {
            "entry": markdown.markdown(util.get_entry(results[0])),
            "title": results[0].capitalize()
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "results": results, 
            "query": query
        })
    
def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_title"]
            content = form.cleaned_data["new_content"]
            if util.get_entry(title) is not None:
                form.add_error('new_title', ValidationError("An entry with this title already exists, please choose a new title"))
            else:
                util.save_entry(title, content)
                return render(request, "encyclopedia/page.html", {
                    "entry": markdown.markdown(util.get_entry(title)),
                    "title": title
                })
        return render(request, "encyclopedia/newpage.html", {
            "form": form
        })

    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewPageForm()
        })
    
def edit(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        form = Edit(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            updated_entry = util.get_entry(title)
        return render(request, "encyclopedia/page.html", {
            "entry": markdown.markdown(updated_entry),
            "title":title.capitalize()
        })
    else:
        form = Edit(initial={'content': entry})
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })
    
def random(request):
    entries = util.list_entries()
    random_page = choice(entries)
    return render(request, "encyclopedia/page.html", {
        "entry": markdown.markdown(util.get_entry(random_page)),
        "title":random_page
    })


