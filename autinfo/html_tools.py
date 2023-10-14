def csrf(html: str) -> str:
    return html.split("var _csrf_token_headers =  {'X-CSRF-TOKEN' : '")[1].split("'")[0]


def change_unicode(student_id: str) -> str:
    {"0": "%DB%B0"}
    return "".join(["%DB%B{}".format(i) for i in str(student_id).strip()])
