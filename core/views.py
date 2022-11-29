from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
    

# -------------------------------------------------VIEWS------------------------------------------------------------------------
def main_menu(request):
    in_items = InDocumentItem.objects.all()
    indocuments = InDocument.objects.all()
    out_items = OutDocumentItem.objects.all()
    outdocuments = OutDocument.objects.all()
    context = {
        # 'in_items':in_items,  
        # 'indocuments':indocuments,
        # 'out_items':out_items,  
        # 'outdocuments':outdocuments,

    }
    return render(request,'core/main_menu.html',context)

def stock_list(request,id):
    if id == 1:
        # first_document = Document.objects.filter(location = "BH").first()
        items = GodownItem.objects.filter(godown__godown_name = 'Bhiwandi')
        total_qty = GodownItem.objects.aggregate(Sum('qty'))
        location = "Bhiwandi"
    elif id == 2:
        # first_document = Document.objects.filter(location = "VS").first()
        items = GodownItem.objects.filter(godown__godown_name = 'Vasai')
        location = "Vasai"
    elif id == 3:
        # first_document = Document.objects.filter(location = "M1").first()
        items = GodownItem.objects.filter(godown__godown_name = 'Haroon Building')
        location = "Haroon Building"
    elif id == 4:
        # first_document = Document.objects.filter(location = "M2").first()
        items = GodownItem.objects.filter(godown__godown_name = "M1")
        location = "Mumbai 1st Floor"
    elif id == 5:
        # first_document = Document.objects.filter(location = "M3").first()
        items = GodownItem.objects.filter(godown__godown_name = "M2")
        location = "Mumbai 2nd Floor"
    elif id == 6:
        # first_document = Document.objects.filter(location = "N").first()
        items = GodownItem.objects.filter(godown__godown_name = "M3")
        location = "Mumbai 3rd Floor"
    elif id ==7:
        items = GodownItem.objects.all()
        location = "All Godowns"
    
    total_qty = items.aggregate(Sum('qty')) # finds sum of a column of a given model, the result is a dict with format dict_name = {'col__aggfunc':value} 2 underscores
    
    context = {
        'total_qty':total_qty['qty__sum'],
        'location':location,
        'items':items
    }
    return render(request,'core/stock_list.html',context)

def document(request):
    documents = Document.objects.all()
    context = {
        'documents':documents
    }
    return render(request,'core/documents.html',context)

def docitems(request,id):
    current_document = Document.objects.get(id = id)
    docitems = DocumentItem.objects.filter(document = current_document)
    context = {
        'document':current_document,
        'docitems':docitems
    }
    return render(request,'core/docitems.html',context)
    
# -------------------------------------------------CREATE---------------------------------------------------------------------------
@login_required
def create_document(request):
    user = request.user
    person = Profile.objects.get(user = user)
    type = request.GET.get('type')
    godown_name = request.GET.get('godown_name')
    form = DocumentForm(initial={'type':type,'person':person,'godown_name':godown_name})
    context = {
        'form':form
    }
    if request.method =="POST":
        form = DocumentForm(request.POST)
        user = request.user 
        profile = Profile.objects.get(id = user.id)
        if form.is_valid():
            form.instance.person = profile
            document = form.save(commit=False)
            document.person = person
            document.save()
            return redirect('create-docitem',id = document.id)
    return render(request,'core/documentform.html',context)

@login_required 
def create_docitem(request,id):
    docitem_formset = inlineformset_factory(Document,DocumentItem,fields=('item','qty'),extra=10)
    # docitem_form = DocumentItemForm(request.POST or None)
    current_document = Document.objects.get(id = id)
    formset = docitem_formset(instance=current_document)
    
    context = {
        'formset':formset,
        'document':current_document
    }
    if request.method == "POST":
        current_document = Document.objects.get(id = id)
        # docitem_form = DocumentItemForm(request.POST or None)
        # docitem_form.instance.document = current_document
        formset = docitem_formset(request.POST,instance=current_document)
        if formset.is_valid():
            formset.save()
            return redirect('docitems',id = current_document.id)
    return render(request,'core/docitemform.html',context)