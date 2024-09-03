from src.domain.entities import PaymentRead

payment_options_en = [
    PaymentRead(id=1, option="cryptocurrency"),
    PaymentRead(id=2, option="bank transfer"),
    PaymentRead(id=3, option="installment"),
]

payment_options_ru = [
    PaymentRead(id=1, option="криптовалюта"),
    PaymentRead(id=2, option="банковский перевод"),
    PaymentRead(id=3, option="рассрочка"),
]

payment_options_de = [
    PaymentRead(id=1, option="Kryptowährung"),
    PaymentRead(id=2, option="Banküberweisung"),
    PaymentRead(id=3, option="Rate"),
]
