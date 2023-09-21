import re
from collections import Counter

with open("example.html", "r") as f:
    html = f.read()

opened_tags = re.findall(r"<([a-z]+)(?![^>]*\/>)[^>]*>", html)
closed_tags = re.findall(r"</([a-z]+)(?![^>]*\/>)[^>]*>", html)
unclosed_tags = list((Counter(opened_tags) - Counter(closed_tags)).elements())
all_tags = re.findall(r"<([^>]+)>", html)


def remove_open_closed_tags(tags):  # ["body.div[0]", "body.div[1]"]
    for index, tag in enumerate(tags):
        max_index = len(tags) - 1
        if index != max_index:
            closed_tag = '/' + tag
            next_tag = tags[index + 1]
            if next_tag == closed_tag:
                # Удаляем пару тегов и вызываем функцию без них
                tags.pop(index)
                tags.pop(index)
                remove_open_closed_tags(tags)
    return tags


def main(tags):
    outer_tags = []
    result = []
    closed_outer_tags = []
    inner_count = 0
    for index, tag in enumerate(tags):
        max_index = len(tags) - 1
        if index != max_index:
            closed_tag = '/' + tag if '/' not in tag else tag
            closed_outer_tags.append(closed_tag)
            next_tag = tags[index + 1]
            closed_last_outer_tag = '/' + outer_tags[-1] if outer_tags else None
            if tag == closed_tag:
                continue
            if next_tag != closed_tag and next_tag != tag and next_tag != closed_last_outer_tag:
                outer_tags.append(tag)
            else:
                outer_tag = ".".join(outer_tags)
                unclosed_tag = f'{outer_tag}.{tag}[{inner_count}]'
                result.append(unclosed_tag)
                inner_count += 1
                if next_tag == closed_last_outer_tag:
                    outer_tags.pop()
    return result


my_tags = remove_open_closed_tags(all_tags)
print(my_tags)
print(main(my_tags))

# print('opened_tags - ', opened_tags)
# print('closed_tags - ', closed_tags)
# print('unclosed_tags - ', unclosed_tags)
# print('all_tags - ', all_tags)
