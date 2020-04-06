from menu.tests.menu_test_base import MenuBaseTest
from menu.forms import MenuForm


class MenuFormTests(MenuBaseTest):
    """
    Test MenuForm user input data
    with valid and invalid scenarios.
    """

    def test_menu_form_valid(self):
        """Form with valid data input"""

        form = MenuForm(data=MenuBaseTest.form_valid_data)
        self.assertTrue(form.is_valid())

    def test_menu_form_invalid_string_length(self):
        """Form with invalid string length (over the maximum)"""

        form = MenuForm(data=MenuBaseTest.form_with_invalid_string_length)
        self.assertFalse(form.is_valid())

    def test_menu_form_invalid_number_of_selected_items(self):
        """Form with invalid number of selected items, below minimum"""

        form = MenuForm(data=MenuBaseTest.form_with_invalid_number_of_selected_items)
        self.assertFalse(form.is_valid())

    def test_menu_form_invalid_expiration_date(self):
        """Form with invalid expiration date"""

        form = MenuForm(data=MenuBaseTest.form_with_invalid_expiration_date)
        self.assertFalse(form.is_valid())

    def test_menu_form_with_existing_season_name(self):
        """Form with existing season name"""
        form = MenuForm(data=MenuBaseTest.form_with_existing_season_name_data)
        self.assertFalse(form.is_valid())
