def reverse_string(text):
    reversed_text = ""

    for index in range(len(text) - 1, -1, -1):
        reversed_text += text[index]

    return reversed_text