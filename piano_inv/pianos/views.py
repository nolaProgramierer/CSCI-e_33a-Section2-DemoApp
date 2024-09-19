from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms


class AddPianoForm(forms.Form):
    brand = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Piano brand",
    })
    )
    finish = forms.CharField(
         widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Piano finish"
    })
    )
    price = forms.IntegerField(
         widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': "Piano price"
    })
    )


def index(request):
    # request.session.flush()
    # Return the piano object if in the session
    pianos = request.session.get('pianos', [])
    return render(request, "pianos/index.html", {"pianos": pianos})


def add_piano(request):
    if request.method == "POST":
        # Add the request data to a blank form
        form = AddPianoForm(request.POST)
        
        # Server side validation
        if form.is_valid():
            # Request data is now contained in the django 'cleaned_data' attribute
            # Converted to python types
            brand = form.cleaned_data["brand"]
            finish = form.cleaned_data["finish"]
            price = form.cleaned_data["price"]
            
            # Combine form entries into python dictionary
            new_piano = {"brand": brand, "finish": finish, "price": price}
            # Retrieve the pianos object from the session
            pianos = request.session.get('pianos', [])

            # Check to see if any element of an iterable meet all conditions
            # if any(expression for item in iterable):
            if any(
                    piano["brand"] == new_piano["brand"] and
                    piano["finish"] == new_piano["finish"] and 
                    piano["price"] == new_piano["price"]
                    for piano in pianos
                ):
                # Add a non-field error to the form
                form.add_error(None, "A piano with these attributes already exists")
                return render(request, "pianos/add_piano.html", {"form": form})
            
            # Append to 'pianos' dictionary array
            pianos.append(new_piano)

            # Add the new pianos object to the session
            request.session['pianos'] = pianos
            # Ensure the session is saved
            request.session.modified = True
            # Return the index page
            return HttpResponseRedirect(reverse("index"))
        
        # If the form isn't valid render the form
        return render(request, "pianos/add_piano.html", {"form": form})
    
    return render(request, "pianos/add_piano.html", { "form": AddPianoForm()})


def piano_detail(request, brand, finish, price):
    # Return sessions piano object
    pianos = request.session.get('pianos', [])
    # Return the 1st element, or None, from the generator expression
    piano = next((
        piano for piano in pianos 
        if (piano['brand'] == brand and 
            piano['finish'] == finish and 
            piano['price'] == price)
    ), None)
             
    # Render the detail page
    return render(request, "pianos/piano_detail.html", {"piano": piano})
    

def edit_piano(request, brand, finish, price):
    # Retrieve piano list from the session
    pianos = request.session.get('pianos', [])

    # Find the piano to edit based on its attributes
    piano_to_edit = next((
    piano for piano in pianos
    if piano["brand"] == brand and piano["finish"] == finish and piano["price"] == price
    ), None)
    
    if not piano_to_edit:
        return render(request, "pianos/piano_not_found.html")
    # Populate the form with form data
    if request.method == "POST":
        form = AddPianoForm(request.POST, initial=piano_to_edit)

        if form.is_valid():
            updated_brand = form.cleaned_data["brand"]
            updated_finish = form.cleaned_data["finish"]
            updated_price = form.cleaned_data["price"]
            
            # Update piano object
            piano_to_edit.update({"brand": updated_brand,
                                 "finish": updated_finish,
                                 "price": updated_price})

            # Save the updated piano list back to the session
            request.session["pianos"] = pianos
            # Ensure session is modified
            request.session.modified = True

            return HttpResponseRedirect(reverse("index"))
        
        else:
            form = AddPianoForm(initial=piano_to_edit)
    return render(request, 
                  "pianos/edit_piano.html", 
                  {"form": AddPianoForm(initial=piano_to_edit), "piano": piano_to_edit}
                  )


def remove_piano(request, brand, finish, price):
    # Return the piano object from the session
    pianos = request.session.get('pianos', [])
    # Formulate new session object without piano
    new_pianos = [
        piano for piano in pianos
        if not (piano['brand'] == brand and 
                piano['finish'] == finish and 
                piano['price'] == price)
    ]
    # Add new piano object to the session
    request.session['pianos'] = new_pianos
    # Redirect to index page
    return HttpResponseRedirect(reverse('index'))