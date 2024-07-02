from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

# pianos = [
#     {"brand": "Steinway", "price": 85000, "finish": "ebony"}
# ]

class AddPianoForm(forms.Form):
    brand = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control flex-item',
            'placeholder': "Piano brand",
    })
    )
    finish = forms.CharField(
         widget=forms.TextInput(attrs={
            'class': 'form-control flex-item',
            'placeholder': "Piano finish"
    })
    )
    price = forms.IntegerField(
         widget=forms.TextInput(attrs={
            'class': 'form-control flex-item',
            'placeholder': "Piano price"
    })
    )


def index(request):
    # request.session.flush()
    pianos = request.session.get('pianos', [])
    return render(request, "pianos/index.html", {"pianos": pianos})


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

            # Retrieve the pianos object from the session
            pianos = request.session.get('pianos', [])
            
            # Append to 'pianos' dictionary array
            pianos.append(new_piano)
            # Print to terminal for testing 
            print(pianos)

            # Add the new pianos object to the session
            request.session['pianos'] = pianos
            # Ensure the session is saved
            request.session.modified = True

            # Return the index page
            return HttpResponseRedirect(reverse("index"))
        
        # If the form isn't valid render the form with invalid entries
        else: return render(request, "pianos/add_piano.html", {"form": form})
    
    return render(request, "pianos/add_piano.html", { "form": AddPianoForm()})
