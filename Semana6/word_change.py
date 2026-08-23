def sort_words_by_dash(text):
    words_list = text.split("-")
    words_list.sort()
    sorted_text = "-".join(words_list)
    return sorted_text



text = "python-para-desarrolladores-de-software"
result = sort_words_by_dash(text)
print(result)