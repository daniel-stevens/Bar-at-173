# core/tests.py
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import User, Drink, Session, Consumption


class BarTests(TestCase):
    def setUp(self):
        # Create some sample data
        self.user = User.objects.create_user(username='alice', password='pass123', first_name='Alice')
        self.drink = Drink.objects.create(name='Test Beer', price_pence=200, color='#AAAAAA')
        self.session = Session.objects.create(name='Test Session', start_time=timezone.now())
        self.session.drinks.add(self.drink)

    def test_log_consumption(self):
        # Ensure no consumption exists initially
        self.assertEqual(Consumption.objects.count(), 0)
        # Simulate logging a drink via the view
        log_url = reverse('log-consumption', args=[self.user.id, self.drink.id])
        response = self.client.post(log_url)
        # After logging, it should redirect back to kiosk page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(reverse('kiosk')))
        # Now one consumption record should exist
        self.assertEqual(Consumption.objects.count(), 1)
        log = Consumption.objects.first()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.drink, self.drink)
        self.assertEqual(log.session, self.session)
        self.assertEqual(log.price_pence, 200)

    def test_scoreboard_data(self):
        # Create a couple of consumption logs
        Consumption.objects.create(user=self.user, drink=self.drink, session=self.session, price_pence=200)
        Consumption.objects.create(user=self.user, drink=self.drink, session=self.session, price_pence=200)
        # Fetch scoreboard page
        url = reverse('scoreboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check that the total count appears in the content
        self.assertContains(response, "Alice")
        self.assertContains(response, "2")  # Alice's total drinks
