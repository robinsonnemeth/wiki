import random
import markdown2
from django.shortcuts import render
from django import forms
from . import util
from django.core.files.storage import default_storage


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title",
                            widget=forms.TextInput(attrs={'class': 'form-control col-md-8 col-lg-8 form-group'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8 form-group', 'rows': 10}))
    edit = forms.BooleanField(widget=forms.HiddenInput)
    titleBefore = forms.CharField(initial="", widget=forms.HiddenInput)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def search(request, name):
    markdowner = markdown2.Markdown()
    searchPage = util.get_entry(name)
    if searchPage is None:
        return render(request, "encyclopedia/notfound.html", {
            "name": name
        })
    else:
        output = markdowner.convert(util.get_entry(name))
        return render(request, "encyclopedia/search.html", {
            "entry": output,
            "name": name
        })


def searchEntry(request):
    markdowner = markdown2.Markdown()
    if request.method == "POST":
        q = request.POST["q"]
        subStringEntries = []
        qCount = 0
        for entry in util.list_entries():
            if q.upper() in entry.upper():
                subStringEntries.append(entry)
                qCount += 1
        if qCount == 0:
            return render(request, "encyclopedia/notfound.html", {
                "name": q
            })
        elif qCount == 1:
            if q.upper() == subStringEntries[0].upper():
                output = markdowner.convert(util.get_entry(q))
                return render(request, "encyclopedia/search.html", {
                    "entry": output,
                    "name": q
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": subStringEntries,
                    "search": True,
                    "name": q
                })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": subStringEntries,
                "search": True,
                "name": q
            })


def newEntryPage(request):
    form = NewEntryForm()
    form.fields["edit"].initial = False
    return render(request, "encyclopedia/newEntry.html", {
        "form": form
    })


def newEntry(request):
    markdowner = markdown2.Markdown()
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        edit = request.POST["edit"]
        titleBefore = request.POST["titleBefore"]
        searchPage = util.get_entry(title)
        if searchPage is None or edit == "True":
            if edit == "True":
                filename = f"entries/{titleBefore}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(title, content)
            output = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/search.html", {
                "entry": output,
                "name": title,
                "duplicate": False
            })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": NewEntryForm(),
                "entry": util.get_entry(title),
                "title": title,
                "duplicate": True
            })
    else:
        return render(request, "encyclopedia/wiki")


def editPage(request, entry):
    contentpage = util.get_entry(entry)
    form = NewEntryForm()
    form.fields["title"].initial = entry
    form.fields["content"].initial = contentpage
    form.fields["edit"].initial = True
    form.fields["titleBefore"].initial = entry
    return render(request, "encyclopedia/newEntry.html", {
        "form": form,
        "name": entry,
        "edit": True
    })


def randomPage(request):
    markdowner = markdown2.Markdown()
    listPages = util.list_entries()
    countPages = int(len(listPages))-1
    pageRandom = random.randint(0, countPages)
    output = markdowner.convert(util.get_entry(listPages[pageRandom]))
    return render(request, "encyclopedia/search.html", {
        "entry": output,
        "name": listPages[pageRandom],
        "duplicate": False
    })
