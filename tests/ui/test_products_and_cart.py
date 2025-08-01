
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






