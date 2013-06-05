import os
import re
import urllib
import datetime
from xml.dom.minidom import parseString

from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import simplejson

from apps.news.models import Category, Article
from apps.contact.forms import PAContactForm
from apps.common.views import simple_dtt

MONTH_MAP = {
    1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July',
    8:'August',
    9:'September',
    10:'October',
    11:'November',
    12:'December',
}

def get_text(node):
    return node[0].firstChild.nodeValue

def news_home(request):
    # latest 5 articles
    articles = Article.objects.order_by('-date_created')[:5]

    # random 4 articles from archive
    random_articles = Article.objects.order_by('?')[:4]

    # grab categories
    categories = Category.objects.order_by('pk')
    
    # grab videos from youtube
    yt_feed = 'http://gdata.youtube.com/feeds/api/playlists/371901C9D9882FB8?v=2'
    xml_feed = urllib.urlopen(yt_feed)
    dom = parseString(xml_feed.read())
    entries = dom.getElementsByTagName('entry')

    videos = []
    for entry in entries:
        description = get_text(entry.getElementsByTagName('media:description'))
        title = get_text(entry.getElementsByTagName('title'))
        views = entry.getElementsByTagName('yt:statistics')[0].getAttribute('viewCount')
        links = entry.getElementsByTagName('link')
        for ylink in links:
            if ylink.getAttribute('rel') == 'alternate':
                link = ylink.getAttribute('href')

        video_group = re.search(r'v=(?P<video_id>.*)&', link, re.I)

        videos.append({'description': description,
                       'title': title,
                       'views': views,
                       'link': link,
                       'id': video_group.groups()[0]})

    return simple_dtt(request, 'news/index.html', {
        'headline': articles[0],
        'articles': articles[1:],
        'last_id': articles[4].pk,
        'videos': videos[:3],
        'random_articles': random_articles,
        'categories': categories,
        'pages': ['support'],
        'page_name': 'news-home'})

def articles(request, **kwargs):
    # get all years and months that have articles
    article_years = Article.objects.dates('date_created',
        'year', order="DESC")

    articles = Article.objects.order_by('-date_created')
    
    if 'year' in kwargs:
        year = kwargs['year']
    else:
        year = '2012'
    articles = articles.filter(date_created__year=year)

    article_months = articles.dates('date_created',
        'month', order="DESC")

    month = False
    if 'month' in kwargs:
        articles = articles.filter(date_created__month=kwargs['month'])
        month = kwargs['month']

    # order them by month
    months = {}
    for article in articles[1:]:
        a_month = article.date_created.month
        if a_month not in months:
            months[a_month] = []
        months[a_month].append(article)
    m_nums = sorted(months.keys(), reverse=True)


    return simple_dtt(request, 'news/archive.html', {
        'year': year,
        'month': month,
        'article_years': article_years,
        'article_months': article_months,
        'headline': articles[0],
        'articles': articles[1:9],
        'months': months,
        'm_nums': m_nums,
        'map': MONTH_MAP,
        'pages': ['support'],
        'page_name': 'news-home'})


def articles_by_year(request, year):
    return articles(request, year=year)

def articles_by_month(request, year, month):
    return articles(request, year=year, month=month)

def category(request, category_name, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404

    articles = category.article_set.order_by('-pk')[:9]

    forms = {}
    forms['basic'] = PAContactForm()
    
    last_id = 0
    for article in articles:
        last_id = article.pk

    return simple_dtt(request, 'news/category.html', {
        'category': category,
        'headline': articles[0],
        'articles': articles[1:],
        'last_id': last_id,
        'pages': ['support'],
        'page_name': 'news-home'})

def article(request, article_title, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404

    # get 4 related articles if there are not 4 related grab
    # the difference in latest articles
    related = article.related()[:4]
    if len(related) < 4:
        drelated = Article.objects.exclude(pk=article.pk).exclude(
            pk__in=[a.pk for a in related]).order_by(
            '-date_created')[:(4-len(related))]

        [related.append(d) for d in drelated]


    return simple_dtt(request, 'news/single-article.html', {
        'article': article,
        'related': related,
        'pages': ['support'],
        'page_name': 'news-home'})

def load_more_articles(request, last_id):
    articles = Article.objects.filter(pk__lt=last_id)
    # if there are options in the get run them here
    if 'year' in request.GET and request.GET['year'] != '':
        articles = articles.filter(date_created__year=request.GET['year'])
    if 'month' in request.GET and request.GET['month'] != '':
        articles = articles.filter(date_created__month=request.GET['month'])
    if 'category' in request.GET and request.GET['category'] != '':
        try:
            category = Category.objects.get(pk=request.GET['category'])
            articles = articles.filter(categories=category)
        except:
            pass
    # cut the slice
    articles = articles.order_by('-pk')[:4]

    # check if there are more articles to load
    last_id = 0
    for article in articles:
        last_id = article.pk
    marticles = Article.objects.filter(pk__lt=last_id).count()
    can_load_more = False
    if marticles > 0:
        can_load_more = True
    t = loader.get_template('news/_partial/news_article_index_snippet.html')
    c = Context({
        'articles': articles,
        'MEDIA_URL': settings.MEDIA_URL
    })
    html = t.render(c)
    response_data = {'html': html, 'response': 'success',
        'can_load_more': can_load_more, 'last_id': last_id}
    return HttpResponse(simplejson.dumps(response_data),
        mimetype="application/json")
    
    

def import_articles(request):

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

def redirect_old(request, article_id):
    from apps.news.redirect import REDIRECT_MAP
    try:
        b_id = REDIRECT_MAP[article_id]
        article = Article.objects.get(brafton_id=b_id)
        return HttpResponsePermanentRedirect(article.get_absolute_url())
    except:
        raise Http404
    raise Http404

def redirect_old_category(request, category_id):
    from apps.news.redirect import REDIRECT_MAP_CATEGORIES
    try:
        b_id = REDIRECT_MAP_CATEGORIES[category_id]
        category = Category.objects.get(brafton_id=b_id)
        return HttpResponsePermanentRedirect(category.get_absolute_url())
    except:
        raise Http404
    raise Http404
