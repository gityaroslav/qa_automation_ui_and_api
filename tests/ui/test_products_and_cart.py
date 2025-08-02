import re


class TestProductsAndCart():
    def test_add_backpack_to_cart_and_verify_badge(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        products_page.add_sauce_labs_backpack_to_cart()

        assert products_page.get_shopping_cart_badge_count() == "1"
        assert not products_page.is_add_backpack_button_displayed(), \
            "Кнопка 'Add to cart' для рюкзака досі відображається після додавання."
        assert products_page.is_remove_backpack_button_displayed(), \
            "Кнопка 'Remove' для рюкзака не відображається після додавання."

    def test_add_random_items_to_cart_and_verify_badge(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        expected_count = products_page.add_random_products_to_cart()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert actual_count == str(expected_count), \
            (f"Кількість товарів у кошику не відповідає очікуваній. "
             f"Очікується '{expected_count}', фактично '{actual_count}'."
             )

    def test_add_random_items_and_verify_cart_contents(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()

        assert str(len(added_products)) == actual_count
        cart_page = products_page.click_shopping_cart_icon()
        assert cart_page.is_cart_page_displayed()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name), \
                f"Товар '{item_name}' не знайдено на сторінці кошика."

    def test_remove_items_from_cart(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        assert str(len(added_products)) == actual_count
        cart_page = products_page.click_shopping_cart_icon()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name), \
                f"Товар '{item_name}' не знайдено на сторінці кошика."
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
        assert str(len(added_products)) == actual_count
        cart_page = products_page.click_shopping_cart_icon()
        for item_name in added_products:
            assert cart_page.is_item_in_cart_by_name(item_name), \
                f"Товар '{item_name}' не знайдено на сторінці кошика."
        checkout_page_1 = cart_page.click_checkout_button()
        checkout_data = checkout_page_1.generate_checkout_data()
        checkout_page_1.fill_checkout_form(checkout_data)
        checkout_page_2 = checkout_page_1.click_continue_button()
        item_total_text = checkout_page_2.get_item_total()
        tax_text = checkout_page_2.get_tax()
        total_text = checkout_page_2.get_total()
        item_total_price = float(re.findall(r'\d+\.\d+', item_total_text)[0])
        tax_rate = float(re.findall(r'\d+\.\d+', tax_text)[0])
        total_price = float(re.findall(r'\d+\.\d+', total_text)[0])
        expected_total = item_total_price + tax_rate
        assert abs(total_price - expected_total) < 0.01, \
            f"Помилка в розрахунку загальної суми. Очікувалося {expected_total}, отримано {total_price}."
        checkout_complete_page = checkout_page_2.click_finish_button()
        assert checkout_complete_page.is_thank_you_displayed()

    def test_checkout_without_zip_code(self, logged_in_standard_user):
        products_page = logged_in_standard_user
        added_products = products_page.add_random_products_to_cart_and_get_names()
        actual_count = products_page.get_shopping_cart_badge_count()
        cart_page = products_page.click_shopping_cart_icon()
        assert str(len(added_products)) == actual_count
        checkout_page_1 = cart_page.click_checkout_button()
        checkout_data = checkout_page_1.generate_checkout_data_with_empty_zip()
        checkout_page_1.fill_checkout_form(checkout_data)
        checkout_page_1.click_continue_button()
        assert checkout_page_1.is_error_message_displayed()
        assert checkout_page_1.get_error_message_text().lower() == "error: postal code is required"
