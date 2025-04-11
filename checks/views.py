from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ReceiptForm, ItemFormSet
from .models import Receipt, Participant

def home(request):
    return render(request, 'checks/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('my_receipts')
    else:
        form = UserCreationForm()
    return render(request, 'checks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('my_receipts')
    else:
        form = AuthenticationForm()
    return render(request, 'checks/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def my_receipts(request):
    receipts = Receipt.objects.filter(owner=request.user)
    return render(request, 'checks/my_receipts.html', {'receipts': receipts})

@login_required
def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.owner = request.user
            receipt.save()
            
            participants = [
                request.POST.get('participant1', '').strip(),
                request.POST.get('participant2', '').strip(),
                request.POST.get('participant3', '').strip()
            ]
            
            for name in participants:
                if name:
                    Participant.objects.create(receipt=receipt, name=name)
            
            formset = ItemFormSet(request.POST, instance=receipt)
            if formset.is_valid():
                formset.save()
            
            return redirect('receipt_detail', pk=receipt.pk)
    else:
        form = ReceiptForm()
        formset = ItemFormSet()
    return render(request, 'checks/create_receipt.html', {
        'form': form,
        'formset': formset
    })

@login_required
def receipt_detail(request, pk):
    receipt = get_object_or_404(
        Receipt.objects.prefetch_related('items', 'participants'),
        pk=pk,
        owner=request.user
    )
    return render(request, 'checks/receipt_detail.html', {'receipt': receipt})