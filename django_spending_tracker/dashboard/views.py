from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from .models import Post, Income, Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #Added here to restrict access to certain views to logged in users only
from django.views.generic import (
    TemplateView,
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

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'  #<app>/<model>_<viewtype>.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incomes = Income.objects.filter(user=self.request.user).order_by('-date')
        expenses = Expense.objects.filter(user=self.request.user).order_by('-date')
        total_monthly_income = sum((income.amount for income in incomes), Decimal('0.00'))
        total_expenses = sum((expense.amount for expense in expenses), Decimal('0.00'))

        context['incomes'] = incomes
        context['expenses'] = expenses
        context['total_monthly_income'] = total_monthly_income
        context['total_expenses'] = total_expenses
        context['remaining_amount'] = total_monthly_income - total_expenses
        return context


class IncomeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Income
    template_name = 'dashboard/income_detail.html'

    def test_func(self):
        income = self.get_object()
        return self.request.user == income.user


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    template_name = 'dashboard/add_income.html'
    fields = ['name', 'amount', 'frequency', 'type', 'gross_net']
    success_url = reverse_lazy('dashboard-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = 'EUR'
        messages.success(self.request, 'Income added successfully.')
        return super().form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Income
    template_name = 'dashboard/income_form.html'
    fields = ['name', 'type', 'currency', 'amount', 'frequency', 'gross_net']
    success_url = reverse_lazy('dashboard-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        income = self.get_object()
        return self.request.user == income.user


class IncomeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Income
    template_name = 'dashboard/income_confirm_delete.html'
    success_url = reverse_lazy('dashboard-home')

    def test_func(self):
        income = self.get_object()
        return self.request.user == income.user


@login_required
def add_income(request):
    return redirect('add_income')


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

