import re
from pprint import pprint

with open("example.html", "r") as f:
    html = f.read()


html_tags = re.findall(r"<([^>]+)>", html)
reversed_tags = html_tags[::-1]


def convert_tag_to_dict(tags):
    unused_closed_tags = []
    result = []

    def _incr_last_closed_tag_child_cnt():
        if unused_closed_tags:
            unused_closed_tags[-1]['child_count'] += 1

    for tag in tags:
        if tag.startswith('/'):
            _incr_last_closed_tag_child_cnt()
            unused_closed_tags.append({'tag_name': tag, 'child_count': 0})
        else:
            closed_tag = '/' + tag
            if unused_closed_tags and unused_closed_tags[-1]['tag_name'] == closed_tag:
                tag_dict = dict(tag_name=tag, child_count=unused_closed_tags[-1]['child_count'],
                                is_closed_tag=True, can_be_parent=True)
                unused_closed_tags.pop()
            else:
                tag_dict = dict(tag_name=tag, is_closed_tag=False, can_be_parent=False)

                _incr_last_closed_tag_child_cnt()
            result.append(tag_dict)

    return list(reversed(result))


converted_tags = convert_tag_to_dict(reversed_tags)


def get_unclosed_tags(tags):
    result = []
    parent_tags = []
    child_tags = {}

    def _incr_child_index(append_child_to_result=False):
        tag_name = tag['tag_name']
        parent = ".".join([p_tag['tag_name'] for p_tag in parent_tags]) + ('.' if parent_tags else '')
        child_index = child_tags.get(parent, {}).get(tag_name, 0)
        child_tags.setdefault(parent, {}).update({tag_name: child_index + 1})

        if append_child_to_result:
            result.append(f"{parent}{tag_name}[{child_index}]")

    def _decr_last_parent_child_cnt():
        if parent_tags:
            parent_tags[-1]['child_count'] -= 1

    for tag in tags:
        can_be_parent = tag['can_be_parent']

        if can_be_parent and tag.get('child_count', 0) > 0:
            _incr_child_index()
            parent_tags.append(tag)
        else:
            if not can_be_parent:
                _incr_child_index(append_child_to_result=True)

            if len(parent_tags) > 1:
                _decr_last_parent_child_cnt()

                if parent_tags[-1]['child_count'] == 0:
                    parent_tags.pop()
                    _decr_last_parent_child_cnt()
                    for prnt in reversed(parent_tags):
                        if prnt['child_count'] == 0:
                            parent_tags.pop()
                            _decr_last_parent_child_cnt()
                        else:
                            break
            elif len(parent_tags) == 1:
                _decr_last_parent_child_cnt()
                if parent_tags[-1]['child_count'] == 0:
                    parent_tags.pop()
                    _decr_last_parent_child_cnt()

    return result


print(get_unclosed_tags(converted_tags))
# print()
# print(reversed_tags)
# print()
# pprint(converted_tags)
