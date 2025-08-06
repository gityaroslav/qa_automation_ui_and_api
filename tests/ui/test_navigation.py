import pytest


class TestNavigation:
    def test_logout_from_burger_menu(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        products_page.click_burger_menu()
        login_page = products_page.click_burger_logout()
        assert login_page.id_login_box_visible()

    @pytest.mark.xfail(reason="UI bug: 'Add to cart' buttons count does not reset after app state clear.")
    def test_reset_app_state_clears_cart(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        initial_add_buttons = products_page.get_count_of_add_to_cart_buttons()
        expected_count = products_page.add_random_products_to_cart()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert actual_count == expected_count
        products_page.click_burger_menu()
        products_page.click_burger_menu_reset()
        cart_after_reset = products_page.get_shopping_cart_badge_count()
        assert cart_after_reset == 0
        final_add_buttons = products_page.get_count_of_add_to_cart_buttons()
        remove_buttons = products_page.get_count_remove_buttons()
        assert final_add_buttons == initial_add_buttons
        assert remove_buttons == 0

