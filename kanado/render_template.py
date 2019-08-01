import os
from jinja2 import Environment, FileSystemLoader

def render_template(template_name_or_list, **context):
    path = '{}/templates/'.format(os.getcwd())
    loader = FileSystemLoader(path)
    env = Environment(loader = loader)
    template = env.get_template(template_name_or_list)
    html = template.render(**context)
    return html