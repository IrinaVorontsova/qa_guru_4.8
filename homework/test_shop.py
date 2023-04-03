"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    cart = Cart()
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity), \
            "Number of products not equal to requested"

        assert product.check_quantity(product.quantity // 2), \
            "Problems with checking if the product is less"

        assert product.check_quantity(product.quantity * 2) is False, \
            "Problems with checking if the product is more"

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(product.quantity)
        assert product.quantity == 0, \
            "The balance is not equal to zero when buying all positions"

        product.buy(product.quantity - 10)
        assert product.quantity == 10, \
            "The rest is not correct"

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert product.buy(product.quantity*2) is ValueError,\
                "No error message when buying a product over the balance"


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_add_product(self, cart, product):
        summ = 13
        cart.add_product(product, summ)
        assert cart.products[product] == summ,\
            f"Quantity of item in cart is not equal to item added {summ}"

        summ = 666
        cart.add_product(product, summ)
        assert cart.products[product] == summ, \
            f"Quantity of item in cart is not equal to item added {summ}"

        summ = product.quantity + 666
        cart.add_product(product, summ)
        assert pytest.raises(ValueError), \
            f"An amount greater than {summ} than quantity in stock did not cause an error"
    def test_cart_remove_product(self, cart, product):
        amount_first = 666
        amount_second = 100
        cart.add_product(product, amount_first)
        cart.remove_product(product, amount_second)
        assert cart.products[product] == amount_first - amount_second,\
            "Incorrect amount of product in cart"

        cart.clear()
        cart.add_product(product, amount_second)
        cart.remove_product(product)
        assert product not in cart.products, \
            "Product uninstall failed"

        cart.clear()
        cart.add_product(product, amount_second)
        cart.remove_product(product, amount_first)
        assert product not in cart.products,\
             "Product uninstall failed"

    def test_cart_clear(self, cart, product):
        cart.add_product(product, 45)
        cart.add_product(product, 2)
        cart.clear()

        assert cart.products == {}, \
           "Failed to empty cart"

    def test_cart_total_price(self, cart, product):
        amount_first = 156
        amount_second = 34
        cart.add_product(product, amount_first)
        cart.add_product(product, amount_second)

        assert cart.get_total_price() == (amount_first + amount_second) * product.price, \
            "Total price is not correct"

    def test_cart_buy(self, cart, product):
        amount_first = 11
        amount_second = 66
        finish_quantity = product.quantity - amount_first - amount_second
        cart.add_product(product, amount_first)
        cart.add_product(product, amount_second)
        cart.buy()

        assert cart.get_total_price() == (amount_first + amount_second) * product.price, \
            "Total price is not correct"
        assert product.quantity == finish_quantity, \
            "Quantity is not correct"

    def test_product_is_not_enough(self, product, cart):
        cart.add_product(product, product.quantity + 100)
        with pytest.raises(ValueError):
            assert cart.buy() is ValueError, \
                "The check for the maximum amount product failed"