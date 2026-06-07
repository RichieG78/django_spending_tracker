"""Views for the spending dashboard and income/expense CRUD pages."""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal, InvalidOperation
import calendar
from .models import Income, Expense
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
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
    """Show the main dashboard with totals, charts, and monthly navigation."""

    template_name = 'dashboard/home.html'  #<app>/<model>_<viewtype>.html

    @staticmethod
    def _calculate_percentage(part, whole):
        """Return a safe percentage and avoid dividing by zero."""
        if whole <= Decimal('0.00'):
            return Decimal('0.00')
        return (part / whole) * Decimal('100')

    def _get_selected_month_year(self):
        """Read month/year from query params and fall back to the current month."""
        now = timezone.localtime()
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')

        try:
            month = int(month) if month is not None else now.month
            year = int(year) if year is not None else now.year
        except (TypeError, ValueError):
            return now.month, now.year

        if month < 1 or month > 12:
            return now.month, now.year

        return month, year

    def get_context_data(self, **kwargs):
        """Build all dashboard values shown in cards, lists, and charts."""
        context = super().get_context_data(**kwargs)
        selected_month, selected_year = self._get_selected_month_year()
        incomes = Income.objects.filter(
            user=self.request.user,
            date__month=selected_month,
            date__year=selected_year,
        ).order_by('-date')
        expenses = Expense.objects.filter(
            user=self.request.user,
            date__month=selected_month,
            date__year=selected_year,
        ).order_by('-date')
        total_monthly_income = sum((income.amount for income in incomes), Decimal('0.00'))
        total_expenses = sum((expense.amount for expense in expenses), Decimal('0.00'))

        fixed_expenses_total = sum((expense.amount for expense in expenses if expense.type == 'fixed'), Decimal('0.00'))
        fun_expenses_total = sum((expense.amount for expense in expenses if expense.type == 'fun'), Decimal('0.00'))
        future_expenses_total = sum((expense.amount for expense in expenses if expense.type == 'future'), Decimal('0.00'))

        fixed_actual_percent = self._calculate_percentage(fixed_expenses_total, total_monthly_income)
        fun_actual_percent = self._calculate_percentage(fun_expenses_total, total_monthly_income)
        future_actual_percent = self._calculate_percentage(future_expenses_total, total_monthly_income)

        context['incomes'] = incomes
        context['expenses'] = expenses
        context['total_monthly_income'] = total_monthly_income
        context['total_expenses'] = total_expenses
        context['remaining_amount'] = total_monthly_income - total_expenses
        context['fixed_actual_percent'] = fixed_actual_percent.quantize(Decimal('0.01'))
        context['fun_actual_percent'] = fun_actual_percent.quantize(Decimal('0.01'))
        context['future_actual_percent'] = future_actual_percent.quantize(Decimal('0.01'))
        context['fixed_actual_bar_width'] = min(fixed_actual_percent, Decimal('100.00')).quantize(Decimal('0.01'))
        context['fun_actual_bar_width'] = min(fun_actual_percent, Decimal('100.00')).quantize(Decimal('0.01'))
        context['future_actual_bar_width'] = min(future_actual_percent, Decimal('100.00')).quantize(Decimal('0.01'))
        profile = self.request.user.profile
        fixed_target_percent = Decimal(profile.fixed_target_percent)
        fun_target_percent = Decimal(profile.fun_target_percent)
        future_target_percent = Decimal(profile.future_target_percent)
        context['fixed_target_percent'] = fixed_target_percent.quantize(Decimal('0.01'))
        context['fun_target_percent'] = fun_target_percent.quantize(Decimal('0.01'))
        context['future_target_percent'] = future_target_percent.quantize(Decimal('0.01'))
        context['fixed_over_target'] = fixed_actual_percent > fixed_target_percent
        context['fun_over_target'] = fun_actual_percent > fun_target_percent
        context['future_over_target'] = future_actual_percent > future_target_percent
        context['selected_month'] = selected_month
        context['selected_year'] = selected_year
        context['selected_month_name'] = calendar.month_name[selected_month]

        previous_month = selected_month - 1 if selected_month > 1 else 12
        previous_year = selected_year if selected_month > 1 else selected_year - 1
        next_month = selected_month + 1 if selected_month < 12 else 1
        next_year = selected_year if selected_month < 12 else selected_year + 1

        context['previous_month'] = previous_month
        context['previous_year'] = previous_year
        context['next_month'] = next_month
        context['next_year'] = next_year
        return context


class IncomeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Show one income record for its owner."""

    model = Income
    template_name = 'dashboard/income_detail.html'

    def test_func(self):
        income = self.get_object()
        return self.request.user == income.user


class IncomeCreateView(LoginRequiredMixin, CreateView):
    """Create a new income record for the logged-in user."""

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
    """Edit an existing income record owned by the current user."""

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
    """Delete an income record owned by the current user."""

    model = Income
    template_name = 'dashboard/income_confirm_delete.html'
    success_url = reverse_lazy('dashboard-home')

    def test_func(self):
        income = self.get_object()
        return self.request.user == income.user


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """Legacy generic expense create view (kept for compatibility)."""

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
    """Shared helpers for type-specific expense pages (fixed/fun/future)."""

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
    """Base create view used by fixed/fun/future expense create pages."""

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
    """Show one expense item and ensure it matches the requested type."""

    model = Expense
    template_name = 'dashboard/expense_detail.html'

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user and expense.type.lower() == self.get_expense_type()


class ExpenseUpdateView(LoginRequiredMixin, UserPassesTestMixin, ExpenseTypedMixin, UpdateView):
    """Edit one expense item while keeping it in its current category."""

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
    """Delete one expense item from its category."""

    model = Expense
    template_name = 'dashboard/expense_confirm_delete.html'
    success_url = reverse_lazy('dashboard-home')

    def test_func(self):
        expense = self.get_object()
        return self.request.user == expense.user and expense.type.lower() == self.get_expense_type()


class FixedExpenseCreateView(ExpenseTypeCreateView):
    """Create a fixed expense."""

    expense_type = 'fixed'


class FunExpenseCreateView(ExpenseTypeCreateView):
    """Create a fun expense."""

    expense_type = 'fun'


class FutureExpenseCreateView(ExpenseTypeCreateView):
    """Create a future expense."""

    expense_type = 'future'


def about(request):
    """Render the static About page."""
    return render(request, 'dashboard/about.html', {'title': 'About'})


@login_required
def add_income(request):
    """Legacy route: redirect to the current income create URL."""
    return redirect('add_income')


@login_required
def add_expense(request):
    """Legacy route: redirect to the current expense create URL."""
    return redirect('add_expense')

