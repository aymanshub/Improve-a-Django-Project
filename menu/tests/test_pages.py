from menu.tests.menu_test_base import MenuBaseTest


class MenuTemplateTests(MenuBaseTest):
    def test_home_page_works(self):
        """Test Home Page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/list_all_current_menus.html')
        self.assertContains(response, 'Soda Fountain')