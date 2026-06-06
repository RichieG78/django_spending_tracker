from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

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