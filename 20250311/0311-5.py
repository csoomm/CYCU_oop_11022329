print(reversed('parrot'))
print(list(reversed('parrot')))

print(''.join(reversed('parrot')))
def reverse_word(word):
    return ''.join(reversed(word))
reverse_word('cosmos')

word_list = ['cosmos', 'radar', 'apple', 'racecar']

def is_palindrome(word):
    return word == reverse_word(word)
for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)