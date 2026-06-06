from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
from .models import Income, Expense
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


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'dashboard/add_expense.html'
    fields = ['name', 'amount', 'frequency', 'type']
    success_url = reverse_lazy('dashboard-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = 'EUR'
        messages.success(self.request, 'Expense added successfully.')
        return super().form_valid(form)


class ExpenseTypedMixin:
    expense_type = None

    def get_expense_type(self):
        return (self.expense_type or 'fixed').lower()

    def get_expense_type_label(self):
        return self.get_expense_type().capitalize()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_type = self.get_expense_type()
        context['expense_type'] = expense_type
        context['expense_type_label'] = self.get_expense_type_label()
        context['detail_url_name'] = f'expense-{expense_type}-detail'
        context['update_url_name'] = f'expense-{expense_type}-update'
        context['delete_url_name'] = f'expense-{expense_type}-delete'
        return context


class ExpenseTypeCreateView(LoginRequiredMixin, ExpenseTypedMixin, CreateView):
    model = Expense
    template_name = 'dashboard/add_expense.html'
    fields = ['name', 'amount', 'frequency']
    success_url = reverse_lazy('dashboard-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = 'EUR'
        form.instance.type = self.get_expense_type()
        messages.success(self.request, f'{self.get_expense_type_label()} expense added successfully.')
        return super().form_valid(form)


class ExpenseDetailView(LoginRequiredMixin, UserPassesTestMixin, ExpenseTypedMixin, DetailView):
    model = Expense
    template_name = 'dashboard/expense_detail.html'

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user and expense.type.lower() == self.get_expense_type()


class ExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, ExpenseTypedMixin, UpdateView):
    model = Expense
    template_name = 'dashboard/expense_form.html'
    fields = ['name', 'currency', 'amount', 'frequency']
    success_url = reverse_lazy('dashboard-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.type = self.get_expense_type()
        return super().form_valid(form)

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user and expense.type.lower() == self.get_expense_type()


class ExpenseDeleteView(LoginRequiredMixin, UserPassesTestMixin, ExpenseTypedMixin, DeleteView):
    model = Expense
    template_name = 'dashboard/expense_confirm_delete.html'
    success_url = reverse_lazy('dashboard-home')

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user and expense.type.lower() == self.get_expense_type()


class FixedExpenseCreateView(ExpenseTypeCreateView):
    expense_type = 'fixed'


class FunExpenseCreateView(ExpenseTypeCreateView):
    expense_type = 'fun'


class FutureExpenseCreateView(ExpenseTypeCreateView):
    expense_type = 'future'


def about(request):
    return render(request, 'dashboard/about.html', {'title': 'About'})


@login_required
def add_income(request):
    return redirect('add_income')


@login_required
def add_expense(request):
    return redirect('add_expense')

