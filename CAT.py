# Write a function to find the longest common prefix string amongst an array of strings.
# If there is no common prefix, return an empty string "".

def longest_prefix_compare(phrase_a, phrase_b):
    max_len = min(len(phrase_a), len(phrase_b))

    for i in range(max_len):
        if phrase_a[i] != phrase_b[i]:
            return phrase_a[:i]
    return phrase_a[:max_len]


def longest_prefix_all(phrases):
    longest_prefix = phrases[0]
    for phrase in phrases[1:]:
        longest_prefix = longest_prefix_compare(longest_prefix, phrase)

    return longest_prefix


phrases = ['flower', 'flawless', 'floor', 'flare']

print(longest_prefix_all(phrases))