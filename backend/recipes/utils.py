from django.http import HttpResponse

from backend.settings import FOODGRAM, SHOPPING_CART


def shopping_list_txt(shopping_dict, user):
    download_cart = SHOPPING_CART.format(username=user.username)
    for ingredient in shopping_dict:
        download_cart += (
                f'{ingredient} '
                f'({shopping_dict[ingredient]["measurement_unit"]}) '
                f'- {shopping_dict[ingredient]["amount"]}\n'
        )
    download_cart += FOODGRAM
    response = HttpResponse(
            download_cart,
            content_type='text/plain;charset=UTF-8',
        )
    response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_cart.txt"'
        )
    return response
