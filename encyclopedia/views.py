from django.shortcuts import render

from . import util
from .markdown_to_html import mk2html


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    entry_text = util.get_entry(entry_name)

    html_title_h1, html_text = mk2html(entry_text)

    return render(request, "encyclopedia/entry.html",{
        "entry_title_h1":html_title_h1,
        "entry_text": html_text
    })