from django import template
from ..models import Blog

register = template.Library()


@register.filter(name='mediapath')
def mediapath(value):
    return value.replace('/media/blog/', '')


@register.simple_tag
def get_blog_media_url(blog_id):
    try:
        blog = Blog.object.get(id=blog_id)
        return blog.preview.url
    except Blog.DoesNotExist:
        return ''
