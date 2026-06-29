def unrepeated(name):
    ch_repeat = {}
    for ch in name:
        if ch in ch_repeat:
            ch_repeat[ch] += 1
        else:
            ch_repeat[ch] = 1

    for ch in ch_repeat:
        if ch_repeat[ch] == 1:
            return ch
    return "_"


def sum_target(nums, target):
    num_dict = {}
    answers = []
    for num in nums:
        num_dict[num] = True
    for num in nums:
        if num_dict[target - num]:
            answers.append([num, target - num])
            num_dict[num] = False

    return answers



if __name__ == '__main__':
    # print(unrepeated('ssww'))
    print(sum_target([1, 3, 4, 6], 7))

