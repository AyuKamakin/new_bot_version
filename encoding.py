def text_to_number(text):
    return int.from_bytes(text.encode(), 'big')


def number_to_text(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode()
