"""Views for the spending dashboard and income/expense CRUD pages."""

from django.shortcuts import render, redirect
from decimal import Decimal
import calendar
from .models import Income, Expense
from .forms import ExpenseCreateForm, IncomeCreateForm
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

class MonthlyFinanceContextMixin:
    """Build shared month-based income/expense context for dashboard pages."""

    active_page = 'dashboard'

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
        """Build all values needed by the dashboard and spending tracker pages."""
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
        yearly_incomes = Income.objects.filter(
            user=self.request.user,
            date__year=selected_year,
        )
        yearly_expenses = Expense.objects.filter(
            user=self.request.user,
            date__year=selected_year,
        )
        total_monthly_income = sum((income.amount for income in incomes), Decimal('0.00'))
        total_expenses = sum((expense.amount for expense in expenses), Decimal('0.00'))
        annual_income = sum((income.amount for income in yearly_incomes), Decimal('0.00'))
        annual_expense = sum((expense.amount for expense in yearly_expenses), Decimal('0.00'))
        annual_net = annual_income - annual_expense

        fixed_expenses_total = sum((expense.amount for expense in expenses if expense.type == 'fixed'), Decimal('0.00'))
        fun_expenses_total = sum((expense.amount for expense in expenses if expense.type == 'fun'), Decimal('0.00'))
        future_expenses_total = sum((expense.amount for expense in expenses if expense.type == 'future'), Decimal('0.00'))

        fixed_annual_total = sum((expense.amount for expense in yearly_expenses if expense.type == 'fixed'), Decimal('0.00'))
        fun_annual_total = sum((expense.amount for expense in yearly_expenses if expense.type == 'fun'), Decimal('0.00'))
        future_annual_total = sum((expense.amount for expense in yearly_expenses if expense.type == 'future'), Decimal('0.00'))

        fixed_actual_percent = self._calculate_percentage(fixed_expenses_total, total_monthly_income)
        fun_actual_percent = self._calculate_percentage(fun_expenses_total, total_monthly_income)
        future_actual_percent = self._calculate_percentage(future_expenses_total, total_monthly_income)

        context['incomes'] = incomes
        context['expenses'] = expenses
        context['total_monthly_income'] = total_monthly_income
        context['total_expenses'] = total_expenses
        context['remaining_amount'] = total_monthly_income - total_expenses
        context['fixed_expenses_total'] = fixed_expenses_total.quantize(Decimal('0.01'))
        context['fun_expenses_total'] = fun_expenses_total.quantize(Decimal('0.01'))
        context['future_expenses_total'] = future_expenses_total.quantize(Decimal('0.01'))
        context['annual_income'] = annual_income.quantize(Decimal('0.01'))
        context['annual_expense'] = annual_expense.quantize(Decimal('0.01'))
        context['annual_net'] = annual_net.quantize(Decimal('0.01'))
        context['fixed_actual_percent'] = fixed_actual_percent.quantize(Decimal('0.01'))
        context['fun_actual_percent'] = fun_actual_percent.quantize(Decimal('0.01'))
        context['future_actual_percent'] = future_actual_percent.quantize(Decimal('0.01'))
        context['fixed_actual_bar_width'] = min(fixed_actual_percent, Decimal('100.00')).quantize(Decimal('0.01'))
        context['fun_actual_bar_width'] = min(fun_actual_percent, Decimal('100.00')).quantize(Decimal('0.01'))
        context['future_actual_bar_width'] = min(future_actual_percent, Decimal('100.00')).quantize(Decimal('0.01'))
        profile = self.request.user.profile
        context['currency_symbol'] = profile.currency_symbol
        fixed_target_percent = Decimal(profile.fixed_target_percent)
        fun_target_percent = Decimal(profile.fun_target_percent)
        future_target_percent = Decimal(profile.future_target_percent)
        context['fixed_target_percent'] = fixed_target_percent.quantize(Decimal('0.01'))
        context['fun_target_percent'] = fun_target_percent.quantize(Decimal('0.01'))
        context['future_target_percent'] = future_target_percent.quantize(Decimal('0.01'))
        fixed_target_amount = (total_monthly_income * fixed_target_percent / Decimal('100')).quantize(Decimal('0.01'))
        fun_target_amount = (total_monthly_income * fun_target_percent / Decimal('100')).quantize(Decimal('0.01'))
        future_target_amount = (total_monthly_income * future_target_percent / Decimal('100')).quantize(Decimal('0.01'))
        context['fixed_target_amount'] = fixed_target_amount
        context['fun_target_amount'] = fun_target_amount
        context['future_target_amount'] = future_target_amount
        context['fixed_left_to_spend'] = (fixed_target_amount - fixed_expenses_total).quantize(Decimal('0.01'))
        context['fun_left_to_spend'] = (fun_target_amount - fun_expenses_total).quantize(Decimal('0.01'))
        context['future_left_to_spend'] = (future_target_amount - future_expenses_total).quantize(Decimal('0.01'))
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
        context['active_page'] = self.active_page

        month_totals = [Decimal('0.00') for _ in range(12)]
        for expense in yearly_expenses:
            month_totals[expense.date.month - 1] += expense.amount

        month_labels = [calendar.month_abbr[index] for index in range(1, 13)]
        context['month_labels'] = month_labels
        context['month_totals'] = [float(amount.quantize(Decimal('0.01'))) for amount in month_totals]
        context['top_expenses'] = yearly_expenses.order_by('-amount', '-date')[:5]
        spend_breakdown_values = [fixed_expenses_total, fun_expenses_total, future_expenses_total]
        context['spend_breakdown_labels'] = ['Fixed', 'Fun', 'Future']
        context['spend_breakdown_values'] = [float(amount.quantize(Decimal('0.01'))) for amount in spend_breakdown_values]

        if total_expenses > Decimal('0.00'):
            context['fixed_spend_share'] = self._calculate_percentage(fixed_expenses_total, total_expenses).quantize(Decimal('0.01'))
            context['fun_spend_share'] = self._calculate_percentage(fun_expenses_total, total_expenses).quantize(Decimal('0.01'))
            context['future_spend_share'] = self._calculate_percentage(future_expenses_total, total_expenses).quantize(Decimal('0.01'))
        else:
            context['fixed_spend_share'] = Decimal('0.00')
            context['fun_spend_share'] = Decimal('0.00')
            context['future_spend_share'] = Decimal('0.00')

        recommendations = []
        if annual_income <= Decimal('0.00'):
            recommendations.append({
                'type': 'info',
                'title': 'Add your income sources',
                'text': 'Log at least one monthly income so SpendWise can generate more accurate guidance.',
            })
        else:
            if annual_expense > annual_income:
                recommendations.append({
                    'type': 'warning',
                    'title': 'You are overspending this year',
                    'text': 'Your yearly spending is above your yearly income. Reduce non-essential categories to rebalance.',
                })

            fixed_ratio = fixed_annual_total / annual_income
            fun_ratio = fun_annual_total / annual_income
            future_ratio = future_annual_total / annual_income

            if fixed_ratio > Decimal('0.60'):
                recommendations.append({
                    'type': 'warning',
                    'title': 'Fixed costs are high',
                    'text': 'Fixed expenses are over 60% of income. Review subscriptions, utilities, and recurring bills.',
                })
            if fun_ratio > Decimal('0.25'):
                recommendations.append({
                    'type': 'info',
                    'title': 'Fun budget is running high',
                    'text': 'Try capping lifestyle spend each month to keep room for future goals.',
                })
            if future_ratio < Decimal('0.15'):
                recommendations.append({
                    'type': 'success',
                    'title': 'Boost your future allocation',
                    'text': 'Consider moving more into future spending to strengthen savings and long-term plans.',
                })

        if not recommendations:
            recommendations.append({
                'type': 'success',
                'title': 'Great momentum',
                'text': 'Your spending pattern is balanced for this year. Keep tracking monthly to stay consistent.',
            })

        context['recommendations'] = recommendations
        return context


class DashboardView(LoginRequiredMixin, MonthlyFinanceContextMixin, TemplateView):
    """Show high-level dashboard cards for income and target chart tracking."""

    template_name = 'dashboard/home.html'
    active_page = 'dashboard'


class SpendingTrackerView(LoginRequiredMixin, MonthlyFinanceContextMixin, TemplateView):
    """Show all expense tracking functionality and month navigation."""

    template_name = 'dashboard/spending_tracker.html'
    active_page = 'spending-tracker'


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
    form_class = IncomeCreateForm
    success_url = reverse_lazy('dashboard-home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = self.request.user.profile.preferred_currency
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
    form_class = ExpenseCreateForm
    success_url = reverse_lazy('spending-tracker')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = self.request.user.profile.preferred_currency
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
    form_class = ExpenseCreateForm
    success_url = reverse_lazy('spending-tracker')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = self.request.user.profile.preferred_currency
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
    success_url = reverse_lazy('spending-tracker')

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
    success_url = reverse_lazy('spending-tracker')

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

