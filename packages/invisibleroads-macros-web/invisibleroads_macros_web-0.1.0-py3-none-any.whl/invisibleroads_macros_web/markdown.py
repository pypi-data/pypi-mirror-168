from markdown import markdown


def get_html_from_markdown(text):
    html = markdown(text)
    clipped_html = html[3:-4]
    if '<p>' not in clipped_html and '</p>' not in clipped_html:
        html = html.removeprefix('<p>')
        html = html.removesuffix('</p>')
    return html
