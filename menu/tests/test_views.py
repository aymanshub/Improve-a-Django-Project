from django.core.urlresolvers import reverse
from menu.tests.menu_test_base import MenuBaseTest


class MenuViewTests(MenuBaseTest):

    def test_existing_menu_detail_view(self):
        """Test for viewing existing menu"""
        response = self.client.get(
            reverse('menu_detail',
                    kwargs={'pk': self.menu1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_detail.html')

    def test_non_existing_menu_detail_view(self):
        """Test for viewing non existing menu"""
        response = self.client.get(
            reverse('menu_detail',
                    kwargs={'pk': self.menu2.pk + 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'menu/menu_detail.html')

    def test_existing_item_detail_view(self):
        """Test for viewing an existing item"""
        response = self.client.get(
            reverse('item_detail',
                    kwargs={'pk': self.item2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/detail_item.html')

    def test_non_existing_item_detail_view(self):
        """Test for viewing non existing item"""
        response = self.client.get(
            reverse('item_detail',
                    kwargs={'pk': self.item2.pk + 10}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'menu/detail_item.html')

    def test_new_menu_view_for_anonymous_user(self):
        """Test Accessing the New MenuForm for Anonymous User"""
        response = self.client.get(
            reverse('menu_new'))
        # 302 is http-status-code-for-resource-which-requires-authorization
        # @login_required redirects to the login page if the user is not logged in
        # hence the view returns 302 in such a case.
        self.assertEqual(response.status_code, 302)

    def test_new_menu_view_logged_in_user(self):
        """Test a new valid MenuForm post request and response."""
        form_addr = reverse('menu_new')
        form_data = MenuBaseTest.form_new_menu_valid_data
        self.client.login(username=self.user.username, password='sirsir')
        response = self.client.post(form_addr,
                                    form_data,
                                    follow=True,
                                    )
        self.assertTemplateUsed(response, 'menu/menu_detail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "menu has been successfully added.")

    def test_edit_menu_view_for_anonymous_user(self):
        """Test Accessing the MenuForm for edit request for Anonymous User"""
        response = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.menu1.pk}))
        # 302 is http-status-code-for-resource-which-requires-authorization
        # @login_required redirects to the login page if the user is not logged in
        # hence the view returns 302 in such a case.
        self.assertEqual(response.status_code, 302)

    def test_edit_menu_view_logged_in_user(self):
        """Test an edit valid MenuForm post request and response."""
        form_addr = reverse('menu_edit', kwargs={'pk': self.menu1.pk})
        form_data_with_a_change = ({
            'season': 'Brunch',
            'items': [self.item1.pk, self.item2.pk],
            'created_date': self.menu1.created_date,
            'expiration_date': self.menu1.expiration_date
        })
        self.client.login(username=self.user.username, password='sirsir')
        response = self.client.post(form_addr,
                                    form_data_with_a_change,
                                    follow=True,
                                    )
        self.assertTemplateUsed(response, 'menu/menu_detail.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, form_data_with_a_change['season'] + ' has been successfully updated.')

    def test_delete_menu_view_for_anonymous_user(self):
        """Test Accessing the DeleteForm for Anonymous User"""
        response = self.client.get(
            reverse('menu_delete', kwargs={'pk': self.menu1.pk}))
        # 302 is http-status-code-for-resource-which-requires-authorization
        # @login_required redirects to the login page if the user is not logged in
        # hence the view returns 302 in such a case.
        self.assertEqual(response.status_code, 302)

    def test_delete_menu_view_for_logged_in_user_with_confirm(self):
        """Test Accessing the DeleteForm with confirm post request and response."""
        self.client.login(username=self.user.username, password='sirsir')
        form_addr = reverse('menu_delete', kwargs={'pk': self.menu1.pk})
        form_data = ({
            'season': self.menu1.season
        })
        response = self.client.post(form_addr,
                                    form_data,
                                    follow=True,
                                    )
        self.assertTemplateUsed(response, 'menu/list_all_current_menus.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.menu1.season + ' menu has been successfully removed.')

