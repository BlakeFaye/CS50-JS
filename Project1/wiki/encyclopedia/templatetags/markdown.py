from django import template
import markdown as md

register = template.Library()

@register.filter(name='convert_md_to_html')
def convert_md_to_html(content):
    return(md.markdown(content))