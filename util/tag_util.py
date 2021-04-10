img_fmts = ['png', 'jpg', 'jpeg', 'tiff', 'gif']
disallowed_tags = ['loli', 'shota', 'underage']

max_field_length = 1024


def is_valid_field_text(text: str):
    if text is None:
        return False

    return 0 < len(text) < max_field_length


def is_video(file_ext: str) -> bool:
    return file_ext not in img_fmts


def contains_disallowed_tags(tags: str) -> bool:
    return any(dt in tags for dt in disallowed_tags)


def parse_tags(tags: str, score: int) -> str:
    if 'score:>' not in tags:
        return f'{tags} score:>{score}'

    return tags
