import datetime
from django.utils import timezone
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.db.models import Q
from menu.models import Menu, Item, Ingredient


class MenuBaseTest(TestCase):
    """
    A base class for the menu app tests
    Including common setUp & data used in various tests
    """
    def setUp(self):
        # for building requests
        self.factory = RequestFactory()
        #  User creation
        self.user = User.objects.create_user(username='Ayman Said', email='example@test.com', password='sirsir')
        self.anonymous_user = AnonymousUser()
        # bulk of ingredients
        self.ingredient1 = Ingredient.objects.create(name='Honey')
        self.ingredient2 = Ingredient.objects.create(name='Lemon')
        self.ingredient3 = Ingredient.objects.create(name='Ginger')
        self.ingredient3 = Ingredient.objects.create(name='Orange')

        self.morning_ingredients = Ingredient.objects.filter(
            Q(name__iexact='Honey') |
            Q(name__iexact='Lemon') |
            Q(name__iexact='Ginger') |
            Q(name__iexact='Orange')
        )
        self.ingredient4 = Ingredient.objects.create(name='Coffee')
        self.ingredient5 = Ingredient.objects.create(name='dark chocolate coffee')
        self.coffee_ingredients = Ingredient.objects.filter(name__icontains='coffee')

        # Morning Drink item
        self.item1 = Item.objects.create(
            name='Morning Drink',
            description='Refreshing drink for body and soul',
            chef=self.user,
            standard=False,
            created_date=timezone.now(),
        )
        self.item1.ingredients.set(self.morning_ingredients)

        # Morning Coffee item
        self.item2 = Item.objects.create(
            name='Morning Coffee',
            description='Arabic Coffee with finest dark chocolate',
            chef=self.user,
            standard=True,
            created_date=timezone.now(),
        )
        self.item2.ingredients.set(self.coffee_ingredients)

        #  Create a menu
        self.menu1 = Menu.objects.create(
            season='Mornings',
            created_date=timezone.now().date(),
            expiration_date=(timezone.now() + datetime.timedelta(days=180)).date()
        )
        self.all_items = Item.objects.all().order_by('name')
        self.menu1.items.set(self.all_items)

        #  Create a menu
        self.menu2 = Menu.objects.create(
            season='Evening',
            created_date=timezone.now(),
            expiration_date=None
        )
        self.all_items = Item.objects.all().order_by('name')
        self.menu2.items.set(self.all_items)

    # Forms data variations:

    form_valid_data = ({
        'season': 'Spring/Summer',
        'items': [1, 2],
        'created_date': datetime.date.today(),
        'expiration_date': datetime.date.today() + datetime.timedelta(days=30)
    })

    form_new_menu_valid_data = ({
        'season': 'Summer',
        'items': [1, 2],
        'created_date': datetime.date.today(),
        'expiration_date': datetime.date.today() + datetime.timedelta(days=30)
    })

    form_with_invalid_string_length = ({
        'season': 'This string length is beyond the max allowed',
        'items': [1, 2],
        'created_date': datetime.date.today(),
        'expiration_date': datetime.date.today() + datetime.timedelta(days=30)
    })

    form_with_invalid_number_of_selected_items = ({
        'season': 'All seasons',
        'items': [1],
        'created_date': datetime.date.today(),
        'expiration_date': datetime.date.today() + datetime.timedelta(days=30)
    })

    form_with_invalid_expiration_date = ({
        'season': 'All seasons',
        'items': [1, 2],
        'created_date': datetime.date.today(),
        'expiration_date': datetime.date.today() - datetime.timedelta(days=30)
    })

    form_with_existing_season_name_data = ({
        'season': 'Mornings',
        'items': [1, 2],
        'created_date': datetime.date.today(),
        'expiration_date': datetime.date.today() - datetime.timedelta(days=30)
    })