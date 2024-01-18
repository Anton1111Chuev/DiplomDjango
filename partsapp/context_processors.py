from partsapp import forms



def get_search_form(request):
    return {'search_form': forms.SearchForm()}

