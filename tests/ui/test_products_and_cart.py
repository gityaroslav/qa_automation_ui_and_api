from pages.products_page import ProductsPage


class TestProductsAndCart():
    def test_add_backpack_to_cart_and_verify_badge(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        products_page.add_sauce_labs_backpack_to_cart()
        assert products_page.get_shopping_cart_badge_count() == 1
        assert not products_page.is_add_backpack_button_displayed()
        assert products_page.is_remove_backpack_button_displayed()

    def test_add_random_items_to_cart_and_verify_badge(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        expected_count = products_page.add_random_products_to_cart()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert actual_count == expected_count

    def test_add_random_items_and_verify_cart_contents(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert len(added_products) == actual_count
        cart_page = products_page.click_shopping_cart_icon()
        assert cart_page.is_cart_page_displayed()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name)

    def test_remove_items_from_cart(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert len(added_products) == actual_count
        cart_page = products_page.click_shopping_cart_icon()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name)
        removed_product = cart_page.remove_random_item_from_cart()
        products_after_remove = cart_page.get_cart_items_names()
        assert len(products_after_remove) == len(added_products) - 1
        assert not cart_page.is_item_in_cart_by_name(removed_product)
        expected_products = [name for name in added_products if name != removed_product]
        assert sorted(products_after_remove) == sorted(expected_products)

    def test_successful_checkout_process(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert len(added_products) == actual_count
        cart_page = products_page.click_shopping_cart_icon()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name)
        checkout_page_1 = cart_page.click_checkout_button()
        checkout_data = checkout_page_1.generate_checkout_data()
        checkout_page_1.fill_checkout_form(checkout_data)
        checkout_page_2 = checkout_page_1.click_continue_button()
        item_total_price = checkout_page_2.get_item_total()
        tax_rate = checkout_page_2.get_tax()
        total_price = checkout_page_2.get_total()
        expected_total = item_total_price + tax_rate
        assert abs(total_price - expected_total) < 0.01
        checkout_complete_page = checkout_page_2.click_finish_button()
        assert checkout_complete_page.is_thank_you_displayed()

    def test_checkout_without_zip_code(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        cart_page = products_page.click_shopping_cart_icon()
        assert len(added_products) == actual_count
        checkout_page_1 = cart_page.click_checkout_button()
        checkout_data = checkout_page_1.generate_checkout_data_with_empty_zip()
        checkout_page_1.fill_checkout_form(checkout_data)
        checkout_page_1.click_continue_button()
        assert checkout_page_1.is_error_message_displayed()
        assert checkout_page_1.get_error_message_text().lower() == "error: postal code is required"

    def test_product_sorting(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        products_page.select_sorting_products_by_value("lohi")
        low_to_high = products_page.get_products_prices()
        products_page.select_sorting_products_by_value("hilo")
        high_to_low = products_page.get_products_prices()
        assert low_to_high == sorted(low_to_high)
        assert high_to_low == sorted(high_to_low, reverse=True)

    def test_random_product(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        product_data_from_list, product_details_page = products_page.select_random_product_and_get_details()
        product_data_from_details = product_details_page.get_all_product_details()
        assert product_data_from_list == product_data_from_details
        products_page_after_return = product_details_page.click_back_to_products_button()
        assert isinstance(products_page_after_return, ProductsPage)


