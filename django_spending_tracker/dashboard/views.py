from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from .models import Post, Income, Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #Added here to restrict access to certain views to logged in users only
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView, #Added here, note if you have a long line of imports you can add ( ) to move each to a new line
    DeleteView #Added here for delete view
)

# Create your views here.
# def home(request):
#     context = {
#        'posts': Post.objects.all()
#     }
#     return render(request, 'dashboard/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'dashboard/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' #<dashboard>/<post>_<list>.html, Now the default name is set equal to 'posts'
    ordering = ['-date_posted'] #Ordering the posts by date in descending order, - sign is used for descending order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['incomes'] = Income.objects.filter(user=self.request.user).order_by('-date')
            context['expenses'] = Expense.objects.filter(user=self.request.user).order_by('-date')
        else:
            context['incomes'] = Income.objects.none()
            context['expenses'] = Expense.objects.none()
        return context


class PostDetailView(DetailView):
    model = Post  


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
     
    #Overriding form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form) # Validate form by running form_valid method from parent class.
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    #Overriding form_valid method 
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author on the form
        return super().form_valid(form) # Validate form by running form_valid method from parent class.
    
    #Added a new function here to check the user author is correct for the specific Post.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # New class PostDeleteView created here
    model = Post
    success_url = '/' # After deleting a post, the user will be redirected to the home page.
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def about(request):
    return render(request, 'dashboard/about.html', {'title': 'About'})


@login_required
def add_income(request):
    if request.method == 'POST':
        amount_raw = request.POST.get('amount', '').strip()
        frequency = request.POST.get('frequency', 'monthly').strip().lower() or 'monthly'
        income_type = request.POST.get('income_type', 'primary').strip().lower() or 'primary'
        other_description = request.POST.get('other_description', '').strip()
        amount_type = request.POST.get('amount_type', 'net').strip().lower() or 'net'

        try:
            amount = Decimal(amount_raw)
            if amount <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            return render(request, 'dashboard/add_income.html', {
                'error_message': 'Please enter a valid amount greater than zero.'
            })

        name = 'Primary Income'
        if income_type == 'other':
            name = other_description or 'Other Income'

        Income.objects.create(
            user=request.user,
            name=name,
            type=income_type,
            currency='EUR',
            amount=amount,
            frequency=frequency,
            gross_net=amount_type,
        )
        messages.success(request, 'Income added successfully.')
        return redirect('dashboard-home')

    return render(request, 'dashboard/add_income.html')


@login_required
def add_expense(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        amount_raw = request.POST.get('amount', '').strip()
        frequency = request.POST.get('frequency', 'monthly').strip().lower() or 'monthly'
        expense_type = request.POST.get('expense_type', 'fixed').strip().lower() or 'fixed'

        if not name:
            return render(request, 'dashboard/add_expense.html', {
                'error_message': 'Please enter an expense name.'
            })

        try:
            amount = Decimal(amount_raw)
            if amount <= 0:
                raise InvalidOperation
        except (InvalidOperation, ValueError):
            return render(request, 'dashboard/add_expense.html', {
                'error_message': 'Please enter a valid amount greater than zero.'
            })

        allowed_types = {'fixed', 'fun', 'future'}
        if expense_type not in allowed_types:
            expense_type = 'fixed'

        Expense.objects.create(
            user=request.user,
            name=name,
            type=expense_type,
            currency='EUR',
            amount=amount,
            frequency=frequency,
        )
        messages.success(request, 'Expense added successfully.')
        return redirect('dashboard-home')

    return render(request, 'dashboard/add_expense.html')

