
class TestNavigation:
    def test_logout_from_burger_menu(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        products_page.click_burger_menu()
        login_page = products_page.click_burger_logout()
        assert login_page.id_login_box_visible()