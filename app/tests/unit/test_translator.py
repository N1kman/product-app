from src.domain.entities import Product
from src.domain.interfaces import Language
from src.infrastructure.translator import MBartTranslator


async def test_translate_from_en_to_ru(get_product_data):
    product = Product(**get_product_data)
    mbart_translator = MBartTranslator()
    tr_product = await mbart_translator.async_translate_obj(
        product,
        Language.en,
        Language.ru
    )
    expected = {
        "name": "молоко",
        "description": "3.2 процента",
        "price": 1.72,
        "category": "category A",
        "manufacturer_id": 4,
        "manufacturer": {
            "country": "Беларусь",
            "tel": "+375447262248",
            "email": "test@test.com"
        }
    }
    print(tr_product)
    assert tr_product == Product(**expected)


async def test_translate_from_en_to_de(get_product_data):
    product = Product(**get_product_data)
    mbart_translator = MBartTranslator()
    tr_product = await mbart_translator.async_translate_obj(
        product,
        Language.en,
        Language.de
    )
    expected = {
        "name": "Milch",
        "description": "3,2 Prozent",
        "price": 1.72,
        "category": "category A",
        "manufacturer_id": 4,
        "manufacturer": {
            "country": "Weißrussland",
            "tel": "+375447262248",
            "email": "test@test.com"
        }
    }
    print(tr_product)
    assert tr_product == Product(**expected)