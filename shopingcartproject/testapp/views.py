from django.shortcuts import render
from testapp.forms import AddItemForm
# Create your views here.
def add_item_view(request):
    form=AddItemForm()
    if request.method=='POST':
        name=request.POST['name']
        quantity=request.POST['quantity']
        request.session[name]=quantity
        request.session.set_expiry(0)

    return render(request,'testapp/additem.html',{'form':form})

def display_item_view(request):
    return render(request,'testapp/displayitem.html')

def session_info_view(request):
    session=request.session
    age=session.get_expiry_age()
    date=session.get_expiry_date()
    print('Expiry age',age)
    print('expiry date',date)
    return render(request,'testapp/additem.html')

