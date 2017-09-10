import random as rand


__author__ = 'grahamstubbs'

FINGERS_SPLAYED = u'\U0001F590'  # This emoji currently only works on mobile
INDEX_POINTING_UP = u'\u261D'
OK_HAND = u'\U0001F44C'
OPEN_HANDS = u'\U0001F450'
RAISED_FIST = u'\u270A'
RAISED_HAND = u'\u270B'
WAVING_HAND = u'\U0001F44B'

EMOJI_LIST = [INDEX_POINTING_UP, OK_HAND, OPEN_HANDS, RAISED_FIST, RAISED_HAND, WAVING_HAND]


def get_random_emoji(last="", next_to_last=""):
    no_last = list(EMOJI_LIST)
    try:
        no_last.remove(last)
    except ValueError:
        pass

    random_emoji = rand.choice(no_last)
    if random_emoji == next_to_last:
        random_emoji = rand.choice(no_last)

    return random_emoji


def get_spaces_list(str_length):
    spaces_list = [0]
    distance = 0
    while distance < str_length:
        num_spaces = 0
        temp_num = rand.randrange(0, 17)
        if temp_num < 2:
            num_spaces = 1
        elif temp_num < 8:
            num_spaces = 2
        elif temp_num < 9:
            num_spaces = 3
        elif temp_num < 15:
            num_spaces = 4
        elif temp_num < 16:
            num_spaces = 6
        else:
            num_spaces = 7

        spaces_list.append(num_spaces)
        distance += num_spaces

    print("spaces_list:")
    print(spaces_list)
    return spaces_list


def trumpify(comment):
    print("comment length: " + str(len(comment)))
    comment_list = comment.split()
    spaces_list = get_spaces_list(len(comment_list))
    output = comment_list[0] + " "

    spaces_idx = 1
    spaces_last_idx = 0
    last_emoji = ""
    next_to_last_emoji = ""

    for i in range(1, len(comment_list)):
        if i - spaces_last_idx == spaces_list[spaces_idx]:
            current_emoji = get_random_emoji(last_emoji, next_to_last_emoji)
            output += current_emoji + " "
            next_to_last_emoji = last_emoji
            last_emoji = current_emoji

            spaces_idx += 1
            spaces_last_idx = i

        output += comment_list[i] + " "

    return output
