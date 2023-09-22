import re
from pprint import pprint

with open("example.html", "r") as f:
    html = f.read()


all_tags = re.findall(r"<([^>]+)>", html)
reversed_all_tags = all_tags[::-1]


def convert_tag_to_dict(tags):
    unused_closed_tags = []
    result = []

    for tag in tags:
        if tag.startswith('/'):
            if unused_closed_tags:
                unused_closed_tags[-1]['child_count'] += 1
            unused_closed_tags.append({'tag_name': tag, 'child_count': 0})
        else:
            closed_tag = '/' + tag
            if unused_closed_tags and unused_closed_tags[-1]['tag_name'] == closed_tag:
                tag_dict = dict(tag_name=tag, child_count=unused_closed_tags[-1]['child_count'],
                                is_closed_tag=True, can_be_parent=True)
                unused_closed_tags.pop()
            else:
                tag_dict = dict(tag_name=tag, is_closed_tag=False, can_be_parent=False)

                if unused_closed_tags:
                    unused_closed_tags[-1]['child_count'] += 1
            result.append(tag_dict)

    return list(reversed(result))


converted_tags = convert_tag_to_dict(reversed_all_tags)


# ["body.div[0]", "body.div[1]"]
def get_unclosed_tags(tags):
    result = []
    parent_stack = []
    child_tags = {}

    for tag in tags:
        tag_name = tag['tag_name']
        can_be_parent = tag['can_be_parent']

        if can_be_parent:
            parent_stack.append(tag)
        else:
            if parent_stack and parent_stack[-1]['child_count'] == 0:
                parent_stack.pop()

            parent = ".".join([tag['tag_name'] for tag in parent_stack]) + ('.' if parent_stack else '')
            child_index = child_tags.get(parent, {}).get(tag_name, 0)
            child_tags.setdefault(parent, {}).update({tag_name: child_index + 1})
            result.append(f"{parent}{tag_name}[{child_index}]")

            if parent_stack:
                parent_stack[-1]['child_count'] -= 1

    return result


print(get_unclosed_tags(converted_tags))
# print()
# print(reversed_all_tags)
# print()
# pprint(converted_tags)
