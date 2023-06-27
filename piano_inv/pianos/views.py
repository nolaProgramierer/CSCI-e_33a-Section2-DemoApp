from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

pianos = [
    {"brand": "Steinway", "price": 85000, "finish": "ebony"}
]

class AddPianoForm(forms.Form):
    brand = forms.CharField(label="Brand: ", max_length=50)
    finish = forms.CharField(label="Finish: ", max_length=50)
    price = forms.IntegerField(label="Price: ")

def index(request):
    context = {"pianos": pianos}
    return render(request, "pianos/index.html", context)


def add_piano(request):
    if request.method == "POST":
        # Add the request data to a blank form
        form = AddPianoForm(request.POST)
        # Server side validation
        if form.is_valid():
            # Request data is now contained in the django 'cleaned_data' attribute
            brand = form.cleaned_data["brand"]
            finish = form.cleaned_data["finish"]
            price = form.cleaned_data["price"]
            # Combine form entries into python dictionary
            new_piano = {"brand": brand, "finish": finish, "price": price}
            # Append to 'pianos' dictionary array
            pianos.append(new_piano)
            print(pianos)
            return HttpResponseRedirect(reverse("index"))
        # If the form isn't valid render the form with invalid entries
        else: return render(request, "pianos/add_piano.html", {"form": form})
    return render(request, "pianos/add_piano.html", { "form": AddPianoForm()})






