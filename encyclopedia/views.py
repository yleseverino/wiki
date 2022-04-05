from tabnanny import check
from venv import create
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
import random

from . import util
from .markdown_to_html import mk2html

class create_entry_form(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-3 mb-3'}),label = "Title")
    mk_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-3'}), label="Text in Markdown")

class edit_entry(forms.Form):
    mk_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mt-3'}), label="Text in Markdown")

def index(request):
    list_entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries
    })

def entry(request, entry_name):
    entry_text = util.get_entry(entry_name)

    if not entry_text:
        return render(request, "encyclopedia/entry.html",{
        "entry_title_h1":'Not found ',
        "not_found": 'ERROR: entry not found 😭'
        }) 

    html_text = mk2html(entry_text)

    return render(request, "encyclopedia/entry.html",{
        "entry_title_h1":entry_name,
        "entry_text": html_text
    })

def edit(request, entry_name):

    if request.method == 'POST':
        form = edit_entry(request.POST)
        if form.is_valid():
            text_markdown = form.cleaned_data["mk_text"]
            util.save_entry(entry_name, text_markdown)
            return redirect(reverse('encyclopedia:entry',args = [entry_name])) 
        else:
            return render(request, "encyclopedia/create_entry.html",{
                "form": form
            })


    entry_text = util.get_entry(entry_name)
    return render(request, "encyclopedia/edit_entry.html",{
        "entry_title_h1":entry_name,
        "form": edit_entry(initial={'mk_text':entry_text})
    })

def random_entry(request):
    list_entries = util.list_entries()
    entry = random.choice(list_entries)

    return redirect(reverse('encyclopedia:entry',args = [entry])) 

def search_entry(request):
    list_entries = util.list_entries()

    search_string = request.GET['q']
    list_searched = [entry for entry in list_entries if search_string.upper() in entry.upper()]

    if search_string.upper() == list_searched[0].upper():
        return redirect(reverse('encyclopedia:entry', args=[list_searched[0]]))

    return render(request, "encyclopedia/index.html", {
        "entries": list_searched,
        "q":search_string
    })

def create_entry(request):

    if request.method == 'POST':
        form = create_entry_form(request.POST)
        if form.is_valid():
            all_title = util.list_entries()
            title_upper = [title.upper() for title in all_title]
            title = form.cleaned_data["title"]
    

            # check_if_title_already_exist
            if title.upper() in title_upper:
                form = create_entry_form()
                return render(request, "encyclopedia/create_entry.html",{
                    "form": form,
                    "alert": 'ERROR: Title already exists 😭'

                })

            text_markdown = form.cleaned_data["mk_text"]

            util.save_entry(title, text_markdown)
            return redirect(reverse('encyclopedia:entry',args = [title])) 
        else:
            return render(request, "encyclopedia/create_entry.html",{
                "form": form
            })



    return render(request, "encyclopedia/create_entry.html",{
        "form": create_entry_form()
    })


