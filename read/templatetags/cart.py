from django import template


register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product , cart):
    keys = cart.keys()
    for name in keys:
        if (name) == (product.name):
            return True
    return False


@register.filter(name='cart_qnty')
def cart_qnty(product , cart):
    keys = cart.keys()
    for name in keys:
        if (name) == (product.name):
            return cart.get(name)
    return 0;


@register.filter(name='price_total')
def price_total(product , cart):
    return product.price * cart_qnty(product , cart)


@register.filter(name='total_cart_price')
def total_cart_price(products , cart ):
    sum = 0 ;
    for p in products:
        sum += price_total(p , cart)
        
    return sum

@register.filter(name='sympol')
def sympol(number):
    return "$" +str(number)

@register.filter(name='multi')
def multi(number1 , number2):
    return number1 * number2

@register.filter(name='total_order_price')
def total_order_price(products , orders ):
    sum = 0 ;
    for p in products:
        sum += price_total(p , orders)
        
    return sum