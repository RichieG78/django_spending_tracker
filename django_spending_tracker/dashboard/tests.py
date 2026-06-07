from decimal import Decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Expense, Income


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_dashboard_requires_auth(self):
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_renders_for_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/home.html')

    def test_dashboard_percentage_context_values(self):
        Income.objects.create(
            name='Salary',
            type='employment',
            amount='1000.00',
            frequency='monthly',
            gross_net='net',
            user=self.user,
        )
        Expense.objects.create(
            name='Rent',
            amount='500.00',
            frequency='monthly',
            type='fixed',
            currency='EUR',
            user=self.user,
        )
        Expense.objects.create(
            name='Cinema',
            amount='300.00',
            frequency='monthly',
            type='fun',
            currency='EUR',
            user=self.user,
        )
        Expense.objects.create(
            name='Savings',
            amount='200.00',
            frequency='monthly',
            type='future',
            currency='EUR',
            user=self.user,
        )

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard-home'))

        self.assertEqual(response.context['fixed_actual_percent'], Decimal('50.00'))
        self.assertEqual(response.context['fun_actual_percent'], Decimal('30.00'))
        self.assertEqual(response.context['future_actual_percent'], Decimal('20.00'))
        self.assertFalse(response.context['fixed_over_target'])
        self.assertFalse(response.context['fun_over_target'])
        self.assertFalse(response.context['future_over_target'])

    def test_dashboard_over_target_flags(self):
        Income.objects.create(
            name='Salary',
            type='employment',
            amount='1000.00',
            frequency='monthly',
            gross_net='net',
            user=self.user,
        )
        Expense.objects.create(
            name='Rent',
            amount='600.00',
            frequency='monthly',
            type='fixed',
            currency='EUR',
            user=self.user,
        )
        Expense.objects.create(
            name='Cinema',
            amount='350.00',
            frequency='monthly',
            type='fun',
            currency='EUR',
            user=self.user,
        )
        Expense.objects.create(
            name='Savings',
            amount='250.00',
            frequency='monthly',
            type='future',
            currency='EUR',
            user=self.user,
        )

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard-home'))

        self.assertTrue(response.context['fixed_over_target'])
        self.assertTrue(response.context['fun_over_target'])
        self.assertTrue(response.context['future_over_target'])

    def test_dashboard_filters_by_selected_month(self):
        june_date = timezone.make_aware(datetime(2026, 6, 15, 12, 0, 0))
        july_date = timezone.make_aware(datetime(2026, 7, 15, 12, 0, 0))

        Income.objects.create(
            name='June Salary',
            type='employment',
            amount='1000.00',
            frequency='monthly',
            gross_net='net',
            user=self.user,
            date=june_date,
        )
        Income.objects.create(
            name='July Salary',
            type='employment',
            amount='2000.00',
            frequency='monthly',
            gross_net='net',
            user=self.user,
            date=july_date,
        )

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard-home'), {'month': 6, 'year': 2026})

        self.assertEqual(response.context['total_monthly_income'], Decimal('1000.00'))
        self.assertEqual(response.context['selected_month_name'], 'June')

    def test_dashboard_month_navigation_rollover(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard-home'), {'month': 1, 'year': 2026})

        self.assertEqual(response.context['previous_month'], 12)
        self.assertEqual(response.context['previous_year'], 2025)
        self.assertEqual(response.context['next_month'], 2)
        self.assertEqual(response.context['next_year'], 2026)


class ExpenseTypedRouteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_add_fun_expense_creates_fun_type(self):
        response = self.client.post(
            reverse('add_fun_expense'),
            {
                'name': 'Cinema',
                'amount': '25.00',
                'frequency': 'monthly',
            },
        )
        self.assertEqual(response.status_code, 302)
        expense = Expense.objects.get(name='Cinema')
        self.assertEqual(expense.type, 'fun')
        self.assertEqual(expense.user, self.user)

    def test_fixed_route_rejects_fun_expense_object(self):
        expense = Expense.objects.create(
            name='Streaming',
            amount=Decimal('12.00'),
            frequency='monthly',
            type='fun',
            currency='EUR',
            user=self.user,
        )
        response = self.client.get(reverse('expense-fixed-detail', kwargs={'pk': expense.pk}))
        self.assertEqual(response.status_code, 403)

    def test_fun_route_rejects_other_user_expense(self):
        expense = Expense.objects.create(
            name='Theme Park',
            amount=Decimal('40.00'),
            frequency='monthly',
            type='fun',
            currency='EUR',
            user=self.other_user,
        )
        response = self.client.get(reverse('expense-fun-detail', kwargs={'pk': expense.pk}))
        self.assertEqual(response.status_code, 403)


class IncomeModelTests(TestCase):
    def test_income_string_representation(self):
        user = User.objects.create_user(username='incomeuser', password='12345')
        income = Income.objects.create(
            name='Salary',
            type='employment',
            amount='5000.00',
            frequency='monthly',
            gross_net='net',
            user=user,
        )
        self.assertIn('Salary', str(income))