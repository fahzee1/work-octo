import os
import urllib
from xml.dom.minidom import parseString

from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import simplejson

from apps.news.models import Category, Article
from apps.contact.forms import PAContactForm


def news_home(request):
    articles = Article.objects.order_by('-date_created')[:5]
    forms = {}
    forms['basic'] = PAContactForm()
    return render_to_response('news/index.html',
        {'forms': forms,
         'headline': articles[0],
         'articles': articles[1:]},
        context_instance=RequestContext(request))

def load_more_articles(request, last_id):
    articles = Article.objects.filter(pk__lt=last_id)[:4]
    t = loader.get_template('news/_partial/news_article_index_snippet.html')
    c = Context({
        'articles': articles,
    })
    html = t.render(c)
    response_data = {'html': html, 'response': 'success'}
    return HttpResponse(simplejson.dumps(response_data),
        mimetype="application/json")
    
    

def import_articles(request):

    def get_text(node):
        return node[0].firstChild.nodeValue

    def get_or_none(model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    feed_url = 'http://feeds.brafton.com/?c43c60b1-3a42-4add-9ec2-5e1e75caad2c'
    xml_feed = urllib.urlopen(feed_url)
    dom = parseString(xml_feed.read())
    dom_articles = dom.getElementsByTagName('Article')
    for article in dom_articles:
        # check to see if the article already exists
        brafton_id = article.getAttribute('ID')
        
        article_obj = get_or_none(Article, brafton_id=brafton_id)
        
        if article_obj is None:
            heading = get_text(article.getElementsByTagName('Heading'))
            content = get_text(article.getElementsByTagName('Contents'))
            summary = get_text(article.getElementsByTagName('Summary'))
            article_obj = Article()
            article_obj.heading = heading
            article_obj.brafton_id = brafton_id
            article_obj.content = content
            article_obj.summary = summary

            # image information
            picture_node = article.getElementsByTagName('Picture')[0]
            if picture_node:
                picture_tag = get_text(picture_node.getElementsByTagName('PhotoTag'))
                picture_url = get_text(picture_node.getElementsByTagName('Large')[0].getElementsByTagName('URL'))
                # were gonna switch the _300.jpg to _500.jpg
                picture_url = picture_url.replace('_300.jpg', '_500.jpg')
                picture_name = picture_url.split('/')[-1]
                local_url = os.path.join(settings.MEDIA_ROOT, 'brafton', picture_name)
                relative_path = os.path.join('brafton', picture_name)
                urllib.urlretrieve(picture_url, local_url)
                article_obj.image = relative_path
                article_obj.image_caption = picture_tag

            article_obj.save()
            
            for category in article.getElementsByTagName('Category'):
                category_id = category.getAttribute('ID')
                category_name = category.firstChild.nodeValue

                # check to see if category exists
                category_obj = get_or_none(Category, brafton_id=category_id)
                
                if category_obj is None:

                    category_obj = Category()
                    category_obj.brafton_id = category_id
                    category_obj.name = category_name
                    category_obj.save()
                article_obj.categories.add(category_obj)

    return HttpResponse('imported')
