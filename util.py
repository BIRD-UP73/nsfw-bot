
img_fmts = ['png', 'jpg', 'jpeg', 'tiff', 'gif']
disallowed_tags = ['loli', 'shota', 'child', 'underage']

max_field_length = 1024


def is_image(ext: str):
    return ext in img_fmts


def contains_disallowed_tags(tags: str):
    for disallowed_tag in disallowed_tags:
        if disallowed_tag in tags:
            return True

    return False


def parse_tags(tags: str, score: int):
    if 'score:>=' not in tags:
        return tags + f' score:>{score}'

    return tags
