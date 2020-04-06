import datetime
from menu.tests.menu_test_base import MenuBaseTest
from menu.models import Menu, Item, Ingredient


class MenuModelTests(MenuBaseTest):
    """
    Testing models:
    - Ingredient
    - Item
    - Menu
    """

    def test_ingredient_model(self):
        """Test ingredient name"""
        orange = Ingredient.objects.get(name='Orange')
        self.assertEqual(str(orange), 'Orange')

    def test_item_model(self):
        """Test item fields"""
        morning_drink = Item.objects.get(name='Morning Drink')
        self.assertEqual(str(morning_drink), 'Morning Drink')
        self.assertEqual(str(morning_drink.chef), 'Ayman Said')
        self.assertIn(str(morning_drink.description), 'Refreshing drink for body and soul')
        for ingredient in morning_drink.ingredients.all():
            self.assertIn(ingredient, Ingredient.objects.all())
        self.assertEqual(morning_drink.ingredients.count(), 4)

    def test_menu_model(self):
        """Test menu fields"""
        morning_menu = Menu.objects.get(season='Mornings')
        self.assertEqual(str(morning_menu), 'Mornings')
        self.assertLess(datetime.date.today(), morning_menu.expiration_date)
        self.assertEqual(morning_menu.items.count(), 2)

