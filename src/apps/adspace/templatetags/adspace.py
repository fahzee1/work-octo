from django import template
from ..models import Ad, Campaign
from django.template import Context, loader

register = template.Library()

# tag syntax {% adspace "ad spot" "sub id(optional)" %}
@register.tag(name="adspace")
def adspace(parser, token):
    try:
        tag_name, ad_spot, sub_id = token.split_contents()
    except ValueError:
        try:
            tag_name, ad_spot = token.split_contents()
            sub_id = None
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (ad_spot[0] == ad_spot[-1] and ad_spot[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    return AdspaceNode(ad_spot, sub_id)

@register.tag
class AdspaceNode(template.Node):

    def __init__(self, ad_spot, sub_id):
        self.ad_spot = ad_spot
        self.sub_id = sub_id

    def render(self, context):  
        t = Ad.objects.filter(type=self.ad_spot.replace('\"',''))[0]
        try:
            ad = t.get_active_campaign()
        except Ad.DoesNotExist:
            return ''
        template = loader.get_template(ad.ad)
        c = Context(context)
        return template.render(c)
