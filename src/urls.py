from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.base import RedirectView
from apps.sitemaps.sitemap import StaticSitemap
from apps.news.sitemaps import ArticleSitemap
from apps.local.sitemaps import KeywordStateSitemap,KeywordSitemapIndex
from django.views.decorators.cache import cache_page, never_cache
from apps.common.views import simple_dtt

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from apps.local.views import LOCAL_KEYWORDS



# a simple direct_to_template wrapper
def dtt(pattern, template, name, parent=None, ctx=None):
    ctx = ctx or {}

    context = dict(page_name=name, parent=parent)
    context.update(ctx)

    return url(pattern, cache_page(60 * 60 * 4)(simple_dtt),
        dict(template=template, extra_context=context),
        name=name)


def dtt_nocache(pattern, template, name, parent=None, ctx=None):
    ctx = ctx or {}

    context = dict(page_name=name, parent=parent)
    context.update(ctx)

    return url(pattern, never_cache(simple_dtt),
        dict(template=template, extra_context=context),
        name=name)
        

sitemaps={
    'home':StaticSitemap(['home','thank_you','sem-landing'],0.5),
    'contact':StaticSitemap(['contact-us','find-us','order-package','privacy-policy'],0.5),
    'shop':StaticSitemap(['shop','copper','bronze','silver','gold','platinum','business','cell-takeover'],0.5),
    'equipment':StaticSitemap(['equipment','home-security-equipment','simon-xt','door-window-sensor','motion-detector',
                                'touchscreen','video','talking-wireless-keypad','garage-door-sensor','glassbreak-sensor',
                                'mini-pinpad','two-button-panic','accessories','simon-3','life-safety-equipment','smoke-detector',
                                'carbon-monoxide-detector','medical-pendant','freeze-sensor','flood-sensor','home-automation-equipment',
                                'door-lock','interactive-control','gps'],0.5),
    'learn':StaticSitemap(['learn','advantage','monitoring','landline','broadband','cellular','about-us','family','charities','payitforward',
                            'payitforward-about','payitforward-press','payitforward-extras','payitforward-rules','payitforward-thankyou','payitforward-teams',
                             'payitforward-spring2012','payitforward-fall2012','payitforward-involved','payitforward-awareness','payitforward-point-scale',
                             'payitforward-revenue','payitforward-video','payitforward-press','learn-about-security','how-it-works','complete-home-security',
                             'testimonials','video-testimonials','send-testimonial','tell-a-friend'],0.5),
    'support':StaticSitemap(['support','installation','operation','troubleshooting','faq','moving-kit','find-us','contact-us','department-listing','feedback-ceo',
                             'careers','jobs','agent-two','affiliate-program','aff'],0.5),
    'help':StaticSitemap(['help','low-price-guarantee','return-policy','state-licenses','do-not-call','security-of-information','warranty'],0.5),
    'thankyou':StaticSitemap(['contact-thank-you','ceo-thank-you','moving-kit-thank-you','contact-tell-friend','affiliate-enroll'],0.5),
    'affiliates':StaticSitemap(['agent-two-lp','package-code','pa-spanish','pa-hialarm','cj','aff','aff-get-started','aff-logos','aff-web-banners','aff-collateral',
                                'aff-products','aff-login'],0.5),
    'seo':StaticSitemap(['seo-home-security-systems','seo-alarm-systems','seo-ge-home-security','seo-ge-home-security-systems','seo-ge-home-security-systems','seo-home-alarm-systems',
                         'seo-security-systems','seo-home-security-systems','seo-best-home-security-system','seo-home-security-companies'],0.5),
    'paidlanding':StaticSitemap(['paid-business-landing-page','paid-adt-copy-cat','paid-adt-copy-cat','paid-adt-comparison-cat','frontpoint-vs-pa','paid-diy-landing-page',
                                 'crime-prevention-month','wireless-landing-page','comcast-vs-protect-america','vivint-vs-protect-america','adt-two','direct-mail'],0.5),
    'crimestoppers':StaticSitemap(['cf-la','cf-chicago','cf-cleveland','cf-miami'],0.5),
    'article':ArticleSitemap,


}        


urlpatterns = patterns('',
    # Example:
    # (r'^protectamerica/', include('protectamerica.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls'))

    # Uncomment the next line to enable the admin:
    # Custom Admin Url
    (r'^django-admin/affiliates/affiliate/add/?$',
        'apps.affiliates.views.add_affiliate'),
    (r'^django-admin/affiliates/affiliate/(?P<affiliate_id>\d+)/?$',
        'apps.affiliates.views.edit_affiliate'),
    (r'^django-admin/', include(admin.site.urls)),

    #newsfeed 
    url(r'^newsfeed/?$', 'apps.common.views.render_feed',name='render-feed'),
    url(r'^hourlycheck/?$', 'apps.newsfeed.views.hourly_check',name='hourly_check'),

    #contact us
    url(r'^contact/ajaxpost/?$', 'apps.contact.views.ajax_post'),
    url(r'^contact-us/?$', 'apps.contact.views.main', name='contact-us'),

    url(r'^contact-us/find-us/?$', 'apps.contact.views.find_us', name='find-us'),
    
    
    url(r'^products/order-package/?$', 'apps.contact.views.order_form',
        name='order-package'),
#    url(r'^sitemap.xml$', 'django.views.generic.simple.direct_to_template', {
#            'template': 'sitemaps/index.xml',
#            'mimetype': 'application/xml',
#        }, name='index'),
    url(r'^sitemap/?', include('apps.pa-sitemaps.urls', namespace='sitemaps')),
    url(r'^support/clear-my-cookies/?$', 'apps.common.views.clear_my_cookies',
        name='clear-my-cookies'),

    # affiliate urls
    #url(r'^affiliate/resources/?$', 'apps.affiliates.views.resources', name='affiliate_resources'),
    #url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/?$', 'apps.affiliates.views.affiliate_view', name='affiliate'),
    #url(r'^affiliate/(?P<affiliate>[a-zA-Z0-9]+)/(?P<page_name>.*)/?$', 'apps.affiliates.views.affiliate_view', name='affiliate_inside'),
    url(r'^sky/?$', 'apps.affiliates.views.delta_sky', name='sky'),
    url(r'^affiliate/', include('apps.affiliates.urls', namespace='affiliates')),
    
    
    # GLOBAL PAGES
    # Help Pages > Privacy Policy
    dtt(r'^help/privacy-policy/?$', 'help/privacy-policy.html', 'privacy-policy', 'help'),

    url(r'^pa/testimonials/(?P<testimonial_id>\d+)/?$',
        'apps.testimonials.views.testimonial',
        name='single-testimonial'),

)

# Radioshack URLS
if settings.SITE_ID == 2:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/radioshack/index.html', 'home', ctx={'page_name': 'index', 'agent_id': 'a02596'}),
        dtt(r'^thank-you/?$', 'affiliates/radioshack/thank-you.html', 'thankyou', ctx={'page_name': 'thankyou', 'agent_id': 'a02596'}),

    )

# Paid landing site
elif settings.SITE_ID == 3:
    urlpatterns += patterns('',
        url(r'^$', 'apps.affiliates.views.semlanding_home'),
        url(r'^google/?$', 'apps.affiliates.views.semlanding_google'),
        url(r'^grbanner/?$', 'apps.affiliates.views.semlanding_google'),
        url(r'^msn/?$', 'apps.affiliates.views.semlanding_bing'),
        dtt(r'^business/?$', 'affiliates/ppc-business-package/index.html', 'paid-business-landing-page'),
        dtt(r'^rep/?$', 'affiliates/sem-landing-page/responsive.html', 'squeeze'),
        dtt(r'^rep/get-quote?$', 'affiliates/sem-landing-page/mobile-quote-form.html', 'squeeze-form'),


    )

elif settings.SITE_ID == 4:
    urlpatterns += patterns('',
        # local pages
        url(r'^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)/?$', 'apps.local.views.local_page',
            name='local-page'),
        url(r'^(?P<state>[A-Z]{2})/?$', 'apps.local.views.local_city',
            name='choose-city'),
        url(r'^(?P<keyword>%s)/sitemap\.xml', 'apps.local.views.sitemap',
            name='keyword-sitemap'),
        url(r'^$', 'apps.local.views.local_state', name='local-state'),
# 301 perm redirect from / to non-/ on article pages
        ('^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)$',
            RedirectView.as_view(url='/%(state)s/%(city)s/',permanent=True)),
    )

elif settings.SITE_ID == 5:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/all-the-things/base.html', 'home', ctx={'page_name': 'index', 'agent_id': 'AllTheThings'}),
    )

# 5 Linx landing site
elif settings.SITE_ID == 6:
    urlpatterns += patterns('',
        dtt_nocache(r'^$', 'affiliates/five-linx/index.html', 'home', ctx={
            'agent_id': 'a01526'}),

        dtt_nocache(r'^copper/?$', 'affiliates/five-linx/copper.html', 'copper', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt_nocache(r'^makes-sense/?$', 'affiliates/five-linx/makes-sense.html', 'makes-sense', 'home', ctx={
            'agent_id': 'a01526'}),
        dtt_nocache(r'^bronze/?$', 'affiliates/five-linx/bronze.html', 'bronze', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt_nocache(r'^silver/?$', 'affiliates/five-linx/silver.html', 'silver', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt_nocache(r'^gold/?$', 'affiliates/five-linx/gold.html', 'gold', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt_nocache(r'^platinum/?$', 'affiliates/five-linx/platinum.html', 'platinum', 'security-packages', ctx={
            'agent_id': 'a01526'}),

        dtt_nocache(r'^video/?$', 'affiliates/five-linx/video.html', 'video', ctx={
            'agent_id': 'a01526'}),

        dtt_nocache(r'^gps/?$', 'affiliates/five-linx/gps.html', 'gps', ctx={
            'agent_id': 'a01526'}),

        dtt_nocache(r'^order/?$', 'affiliates/five-linx/order.html', 'order', ctx={
            'agent_id': 'a01526'}),

        dtt_nocache(r'^thank-you/5linx/?$', 'affiliates/five-linx/thank-you.html', 'thank-you', ctx={
            'agent_id': 'a01526'}),
    )

elif settings.SITE_ID == 7:
    urlpatterns += patterns('',
        url(r'^', include('apps.blogredirects.urls')),
    )

# Tomboy Tools landing site
elif settings.SITE_ID == 8:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/tomboy-tools/index.html', 'home', ctx={
            'agent_id': 'a03169'}),
        dtt(r'^copper$', 'affiliates/tomboy-tools/copper.html', 'copper', 'security-packages', ctx={
            'agent_id': 'a03169'}),
        dtt(r'^bronze$', 'affiliates/tomboy-tools/bronze.html', 'bronze', 'security-packages', ctx={
            'agent_id': 'a03169'}),
        dtt(r'^silver$', 'affiliates/tomboy-tools/silver.html', 'silver', 'security-packages', ctx={
            'agent_id': 'a03169'}),
        dtt(r'^gold$', 'affiliates/tomboy-tools/gold.html', 'gold', 'security-packages', ctx={
            'agent_id': 'a03169'}),
        dtt(r'^platinum$', 'affiliates/tomboy-tools/platinum.html', 'platinum', 'security-packages', ctx={
            'agent_id': 'a03169'}),

        dtt(r'^video$', 'affiliates/tomboy-tools/video.html', 'video', ctx={
            'agent_id': 'a03169'}),

        dtt(r'^gps$', 'affiliates/tomboy-tools/gps.html', 'gps', ctx={
            'agent_id': 'a03169'}),

        dtt(r'^order$', 'affiliates/tomboy-tools/order.html', 'order', ctx={
            'agent_id': 'a03169'}),

        dtt(r'^thank-you/tomboy-tools/?$', 'affiliates/tomboy-tools/thank-you.html', 'thank-you', ctx={
            'agent_id': 'a03169'}),

    )

# Mobile Website
elif settings.SITE_ID == 9:
    urlpatterns += patterns('',
        url(r'^$', 'apps.pricetable.views.index', name='home'),
        url(r'^promo/click-here/?$', 'apps.pricetable.views.test_click', name='home'),
        url(r'^promo/click-call/?$', 'apps.pricetable.views.test_call', name='home'),
        url(r'^promo/click-order/?$', 'apps.pricetable.views.test_order', name='home'),


        url(r'^home-security-packages/?$', 'apps.pricetable.views.packages', name='packages'),
        url(r'^security-add-ons/?$', 'apps.pricetable.views.adds', name='add-ons'),
        url(r'^home-security/?$', 'apps.pricetable.views.home_security', name='home-security'),
        url(r'^home-security-monitoring/?$', 'apps.pricetable.views.monitoring', name='monitoring'),
        url(r'^interactive-monitoring-features/?$', 'apps.pricetable.views.interactive', name='interactive'),
        url(r'^customer-info/?$', 'apps.pricetable.views.customer_info', name='customer-info'),

        url(r'^request-quote/?$', 'apps.pricetable.views.quote', name='get-quote'),
        url(r'^cart/?$', 'apps.pricetable.views.mobile_cart', name='cart'),
        url(r'^add-to-cart/?$', 'apps.pricetable.views.add_to_cart', name='add_to_cart'),
        url(r'^remove-from-cart/?$', 'apps.pricetable.views.remove_from_cart', name='remove_from_cart'),
        url(r'^cart-checkout/?$', 'apps.pricetable.views.mobile_cart_checkout', name='cart-checkout'),
        url(r'^thank-you/?$', 'apps.pricetable.views.thank_you', name='thank_you'),
    )

# Black Friday Site
elif settings.SITE_ID == 10:
    urlpatterns += patterns('',
        url(r'^$', 'apps.common.views.black_friday', name='index'),
    )

# GetAHomeSecuritySystem.com
elif settings.SITE_ID == 11:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/get-a-home-security-system/index.html', 'home'),
    )

# AlarmZone.com
elif settings.SITE_ID == 12:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/alarm-zone/index.html', 'home', ctx={'agent_id': 'a01415'}),
        dtt(r'^shop-home-security/?$', 'external/alarm-zone/shop.html', 'shop', ctx={'agent_id': 'a01415'}),
        dtt(r'^home-alarm-monitoring-services/?$', 'external/alarm-zone/monitoring.html', 'monitoring', ctx={'agent_id': 'a01415'}),
        dtt(r'^ge-security-equipment/?$', 'external/alarm-zone/equipment.html', 'equipment', ctx={'agent_id': 'a01415'}),
        dtt(r'^thank-you/?$', 'external/alarm-zone/thanks.html', 'thank_you', ctx={'agent_id': 'a01415'}),
    )

# SecuritySystemExpert.com
elif settings.SITE_ID == 13:
    urlpatterns += patterns('',
        url(r'^$', 'apps.faqs.views.expert_home', name='home'),
        url(r'^ask/?$', 'apps.faqs.views.ask_question', name='ask_question'),
    )

# Canada
elif settings.SITE_ID == 14:
    urlpatterns += patterns('',
        dtt(r'^$', 'canada/index.html', 'home'),
        dtt(r'^shop/home-security-systems/?$', 'canada/packages.html', 'shop'),
        url(r'^shop/order/?$', 'apps.contact.views.order_form_ca', name='order-package-ca'),
        dtt(r'^thank-you/?$', 'thank-you/canada.html', 'thank_you'),

        # Canada Competitor Landing Pages
        dtt(r'^security-comparison/adt-vs-protect-america/?$', 'affiliates/adt-comparison-canada/index.html', 'home'),
        dtt(r'^security-comparison/reliance-vs-protect-america/?$', 'affiliates/reliance-vs-pa-canada/index.html', 'home'),
        dtt(r'^security-comparison/vivint-vs-protect-america/?$', 'affiliates/vivint-vs-protectamerica-canada/index.html', 'home'),
        dtt(r'^security-comparison/alarmforce-vs-protect-america/?$', 'affiliates/alarmforce-vs-pa-canada/index.html', 'home'),
    )

# BuyaSecuritySystem.com
elif settings.SITE_ID == 15:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/buy-a-security-system/index.html', 'home'),
    )

# GreatHomeSecurityOffer.com
elif settings.SITE_ID == 16:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/great-home-security-offer/index.html', 'home'),
    )

# AlarmSystemOffers.com
elif settings.SITE_ID == 17:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/alarm-system-offers/index.html', 'home'),
    )

# homesecuritycompared.com
elif settings.SITE_ID == 18:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/home-security-compared/index.html', 'home'),
    )

# getfreesecurity.com
elif settings.SITE_ID == 19:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/get-free-security/index.html', 'home'),
    )

# simonxtinstall.com
elif settings.SITE_ID == 20:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/simon-xt-install/index.html', 'home'),
        dtt(r'^thank-you/$', 'external/simon-xt-install/thanks.html', 'thank_you'),
    )

# nationalhomesecuritycompany.com
elif settings.SITE_ID == 21:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/national-home-security-company/index.html', 'home'),
        dtt(r'^thank-you/$', 'external/national-home-security-company/thanks.html', 'thank_you'),
    )

# homesecuritysystemexperts.com
elif settings.SITE_ID == 22:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/homesecuritysystemexperts/index.html', 'home'),
        dtt(r'^thank-you/$', 'external/homesecuritysystemexperts/thanks.html', 'thank_you'),
    )

# freecrimestats.com
elif settings.SITE_ID == 23:
    urlpatterns += patterns('',

        # Direct-To-Template Pages
        dtt(r'^thanks/$', 'external/freecrimestats/thanks.html', 'thanks'),
        dtt(r'^about/$', 'external/freecrimestats/about.html', 'about'),
        dtt(r'^advice/$', 'external/freecrimestats/advice.html', 'advice'),
        dtt(r'^contact/$', 'external/freecrimestats/contact.html', 'contact'),

        url(r'^free-crime-stats/sitemap.xml$',
            'apps.crimedatamodels.views.state_sitemap',
            name='state_sitemap'),
        url(r'^free-crime-stats/(?P<state>\w+)/sitemap.xml$',
            'apps.crimedatamodels.views.city_sitemap',
            name='city_sitemap'),
        url(r'^free-crime-stats/(?P<state>\w+)/(?P<city>[\w\-]+)/sitemap.xml$',
            'apps.crimedatamodels.views.crime_sitemap',
            name='crime_sitemap'),

        # Search Results (.../search/)
        url(r'^search/?$',
            'apps.crimedatamodels.views.search', name='search'),

        # Local Crime Page (.../[State]/[City]/[Crime]/)
        url(r'^(\w{2})/([\w\-]+)/([\w\-]+)/?$',
            'apps.crimedatamodels.views.crime', name='crime'),

        # Local City Page (.../[State]/[City]/)
        url(r'^(?P<state>\w{2})/(?P<city>[\w\-]+)/?$',
            'apps.crimedatamodels.views.local', name='local'),

        # City Listing (.../[State]/)
        url(r'^(\w{2})/?$',
            'apps.crimedatamodels.views.cities', name='cities'),

        # State Listing (.../states/)
        url(r'^states/?$',
            'apps.crimedatamodels.views.states', name='states'),

        # Main Index
        url(r'^$',
            'apps.crimedatamodels.views.home', name='home'),

    )

# defaults
else:
    urlpatterns += patterns('',


        # Test Pages

        # Home Page
        url(r'^$', 'apps.common.views.index', name='home'),
        url(r'^thank-you/?$', 'apps.common.views.thank_you',
            name='thank_you'),
        dtt(r'^404/?$', '404.html', '404', 'home'),

        # Shop
        dtt(r'^shop/?$', 'packages/index.html', 'shop'),

            # Product > Packages

            dtt(r'^shop/copper-package/?$', 'packages/copper.html', 'copper', 'shop'),
            dtt(r'^shop/bronze-package/?$', 'packages/bronze.html', 'bronze', 'shop'),
            dtt(r'^shop/silver-package/?$', 'packages/silver.html', 'silver', 'shop'),
            dtt(r'^shop/gold-package/?$', 'packages/gold.html', 'gold', 'shop'),
            dtt(r'^shop/platinum-package/?$', 'packages/platinum.html', 'platinum', 'shop'),
            dtt(r'^shop/business-package/?$', 'packages/business.html', 'business', 'shop'),
            dtt(r'^shop/existing-security-system/?$', 'products/cell-takeover/index.html', 'cell-takeover', 'shop'),


        # Equipment
            dtt(r'^equipment/?$', 'products/equipment/index.html', 'equipment'),
            
            # Equipment > Home Security
                dtt(r'^equipment/home-security/?$', 'products/equipment/home-security.html', 'home-security-equipment', 'equipment'),
                
                    dtt(r'^equipment/home-security/ge-simon-xt/?$', 'products/equipment/simon-xt.html', 'simon-xt', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/door-window-sensor/?$', 'products/equipment/door-window-sensor.html', 'door-window-sensor', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/motion-detector/?$', 'products/equipment/motion-detector.html', 'motion-detector', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/touchscreen/?$', 'products/equipment/touchscreen.html', 'touchscreen', 'home-security-equipment'),
                    dtt(r'^pa/wireless-security-camera/ip-security-cameras/?$', 'products/equipment/video.html', 'video', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/talking-wireless-keypad/?$', 'products/equipment/talking-wireless-keypad.html', 'talking-wireless-keypad', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/garage-door-sensor/?$', 'products/equipment/garage-door-sensor.html', 'garage-door-sensor', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/glassbreak-sensor/?$', 'products/equipment/glassbreak-sensor.html', 'glassbreak-sensor', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/mini-pinpad/?$', 'products/equipment/mini-pinpad.html', 'mini-pinpad', 'home-security-equipment'),
                    dtt(r'^equipment/home-security/two-button-panic/?$', 'products/equipment/two-button-panic.html', 'two-button-panic', 'home-security-equipment'),
                    dtt(r'^products/security-equipment/accessories/?$', 'products/equipment/security-accessories.html', 'accessories', 'home-security-equipment'),


                    
                    # Moratorium 
                        dtt(r'^equipment/home-security/ge-simon-3/?$', 'products/equipment/simon-3.html', 'simon-3', 'home-security-equipment'),
                        dtt(r'^equipment/home-security/secret-keypad/?$', 'products/equipment/secret-keypad.html', 'secret-keypad', 'home-security-equipment'),
   
            # Life Safety
                dtt(r'^equipment/life-safety/?$', 'products/equipment/life-safety.html', 'life-safety-equipment', 'equipment'),

                    dtt(r'^equipment/life-safety/smoke-detector/?$', 'products/equipment/smoke-detector.html', 'smoke-detector', 'life-safety-equipment'),
                    dtt(r'^equipment/life-safety/carbon-monoxide-detector/?$', 'products/equipment/carbon-monoxide-detector.html', 'carbon-monoxide-detector', 'life-safety-equipment'),
                    dtt(r'^equipment/life-safety/medical-pendant/?$', 'products/equipment/medical-pendant.html', 'medical-pendant', 'life-safety-equipment'),

                    dtt(r'^equipment/life-safety/freeze-sensor/?$', 'products/equipment/freeze-sensor.html', 'freeze-sensor', 'life-safety-equipment'),
                    dtt(r'^equipment/life-safety/flood-sensor/?$', 'products/equipment/flood-sensor.html', 'flood-sensor', 'life-safety-equipment'),
            
            # Equipment > Home Automation
                dtt(r'^equipment/home-automation/?$', 'products/equipment/home-automation.html', 'home-automation-equipment', 'equipment'),
                        dtt(r'^equipment/home-automation/z-wave-door-lock/?$', 'products/equipment/door-lock.html', 'door-lock', 'home-automation-equipment'),

            
            # SMART Connect

                    dtt(r'^equipment/smart-connect-app/?$', 'products/interactive/index.html', 'interactive-control', 'equipment'),
            
            # Equipment > Automotive
        
                    dtt(r'^pa/vehicle-gps-tracking/gps-services/?$', 'products/gps/index.html', 'gps', 'equipment'),


            

        # Learn
            dtt(r'^learn-about-security/?$', 'learn/index.html', 'learn'),

            # Learn > Security Advantage
            dtt(r'^security-advantage/?$', 'products/advantage.html', 'advantage', 'shop'),

            # Learn > Monitoring
            dtt(r'^learn-about-security/monitoring/security-system/?$', 'products/monitoring/index.html', 'monitoring', 'learn'),

                dtt(r'^products/alarm-monitoring/landline/?$', 'products/monitoring/landline.html', 'landline', 'monitoring'),
                dtt(r'^products/alarm-monitoring/broadband/?$', 'products/monitoring/broadband.html', 'broadband', 'monitoring'),
                dtt(r'^products/alarm-monitoring/cellular/?$', 'products/monitoring/cellular.html', 'cellular', 'monitoring'),
            
            # Learn > About Us
                dtt(r'^learn-about-security/protect-america/?$', 'about-us/index.html', 'about-us', 'learn'),
                    url(r'^pa/family-of-companies/america-protect/?$', 'apps.common.views.family_of_companies', name='family'),
                    dtt(r'^pa/charities/america-protect/?$', 'about-us/charities.html', 'charities', 'about-us'),
                    dtt(r'^payitforward/?$', 'payitforward/payitforward.html', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/about/?$', 'payitforward/about.html', 'payitforward-about', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/press/?$', 'payitforward/press.html', 'payitforward-press', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/extras/?$', 'payitforward/extras.html', 'payitforward-extras', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/rules/?$', 'payitforward/rules.html', 'payitforward-rules', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/thankyou/?$', 'payitforward/thankyou.html', 'payitforward-thankyou', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/teams/?$', 'payitforward/teams.html', 'payitforward-teams', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/teams/2012/spring/?$', 'payitforward/spring2012.html', 'payitforward-spring2012', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/teams/2012/fall/?$', 'payitforward/fall2012.html', 'payitforward-fall2012', 'payitforward', ctx={'agent_id': 'i03237'}),
                        url(r'^payitforward/involved/?$', 'apps.contact.views.payitforward', name='payitforward-involved'),
                        url(r'^payitforward/point-tracking/?$', 'apps.payitforward.views.point_tracking', name='payitforward-point-tracking'),
                        dtt(r'^payitforward/awareness/?$', 'payitforward/awareness.html', 'payitforward-awareness', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/point-scale/?$', 'payitforward/point-scale.html', 'payitforward-point-scale', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/revenue/?$', 'payitforward/revenue.html', 'payitforward-revenue', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/video/?$', 'payitforward/video.html', 'payitforward-video', 'payitforward', ctx={'agent_id': 'i03237'}),
                        dtt(r'^payitforward/press/?$', 'payitforward/press.html', 'payitforward-press', 'payitforward', ctx={'agent_id': 'i03237'}),

            # Learn > Security 101
                dtt(r'^pa/learn/alarm-companies/?$', 'about-us/learn-about-security.html', 'learn-about-security', 'about-us'),
                    dtt(r'^pa/how_it_works/ge-security-systems/?$', 'about-us/how-it-works.html', 'how-it-works', 'about-us'),
                    dtt(r'^complete-home-security/?$', 'complete-home-security/index.html', 'complete-home-security'),

            # Learn > Reviews
            url(r'^pa/testimonials/?$', 'apps.testimonials.views.view_testimonials', name='testimonials'),
                url(r'^video-testimonials/?$', 'apps.testimonials.views.view_vidimonials', name='video-testimonials'),
                    url(r'^video-testimonials/(?P<testimonial_id>\d+)/?$', 'apps.testimonials.views.vidimonial', name='single-video-testimonial'),
                url(r'^pa/share-your-testimonial/?$','apps.testimonials.views.send_testimonial', name='send-testimonial'), 
                url(r'^pa/cust_ref/?$','apps.contact.views.tell_a_friend',name='tell-a-friend'),
                               
                # Remove dtt(r'^products/security-equipment/sensors/?$', 'products/equipment/security-sensors.html', 'sensors', 'equipment'),
                # remove dtt(r'^products/interactive-video/home-video-cameras?$', 'products/video/video-home.html', 'video-home', 'video'),
                # remove dtt(r'^products/interactive-video/business-video-cameras?$', 'products/video/video-business.html', 'video-business', 'video'),
                # remove dtt(r'^pa/profile/home-alarm-systems/?$', 'about-us/profile.html', 'profile', 'about-us'),


        # Support
            dtt(r'^support/?$', 'support/index.html', 'support'),
                
                # Support > Customer Service
                    dtt(r'^support/customer-service/?$', 'support/customer-service.html', 'customer-service', 'support'),
                    dtt(r'^support/customer-service/installation/?$', 'support/installation.html', 'installation', 'customer-service'),
                    dtt(r'^support/customer-service/operation/?$', 'support/operation.html', 'operation', 'customer-service'),
                    dtt(r'^support/customer-service/troubleshooting/?$', 'support/troubleshooting.html', 'troubleshooting', 'customer-service'),
                    dtt(r'^support/customer-service/faq/?$', 'support/faq.html', 'faq', 'customer-service'),                
                    url(r'^pa/request-moving-kit/security-moving-kit/?$', 'apps.contact.views.moving_kit', name='moving-kit'),
                    
                # Support > Find Us
                dtt(r'^support/find-us/?$', 'contact-us/find-us.html', 'find-us', 'support'),

                # Support > Contact Us
                url(r'^pa/contact/?$', 'apps.contact.views.main', name='contact-us'),
                    dtt(r'^contact/department-listing/?$', 'contact-us/department-listing.html', 'department-listing', 'contact-us'),
                    url(r'^pa/feedback/?$', 'apps.contact.views.ceo', name='feedback-ceo'),


                # Support > Careers
                url(r'^contact/careers/?$', 'apps.events.views.careers', name='careers'),
                    dtt(r'^contact/careers/job-openings?$', 'contact-us/jobs.html', 'jobs', 'careers'),


                
                # Support > Dealer Program
                dtt(r'^agent-2/?$', 'contact-us/agent-2.html', 'agent-two', 'contact-us'),
                
                # Support > Affiliate Program
                url(r'^contact/affiliate-program/?$', 'apps.affiliates.views.signup', name='affiliate-program'),
                    dtt(r'^affiliate/resources/?$', 'affiliates/resources.html', 'aff'),
                    
        # Help Pages

        dtt(r'^help/?$', 'help/index.html', 'help'),

            # Help Pages > Low Price Guarantee
                dtt(r'^help/low-price-guarantee/?$', 'help/low-price-guarantee.html', 'low-price-guarantee', 'help'),

            # Help Pages > Return Policy
                dtt(r'^help/return-policy/?$', 'help/return-policy.html', 'return-policy', 'help'),

            # Help Pages > State Licenses
                dtt(r'^help/state-licenses/?$', 'help/state-licenses.html', 'state-licenses', 'help'),

            # Help Pages > Do Not Call
                #dtt(r'^help/do-not-call/?$', 'help/do-not-call.html', 'do-not-call', 'help'),
                url(r'^help/do-not-call/?$', 'apps.contact.views.donotcall',
                    name='do-not-call'),
            # Help Pages > Security of Information
                dtt(r'^help/security-of-information/?$', 'help/security-of-information.html', 'security-of-information', 'help'),

            # Help Pages > Warranty
                dtt(r'^help/warranty/?$', 'help/warranty.html', 'warranty', 'help'),

        # Thank You Pages
        dtt(r'^thank-you/contact-us/?$', 'thank-you/contact-us.html', 'contact-thank-you', 'thank-you'),
        dtt(r'^thank-you/ceo/?$', 'thank-you/ceo-thank-you.html', 'ceo-thank-you', 'thank-you'),
        dtt(r'^thank-you/moving-kit/?$', 'thank-you/moving-kit.html', 'moving-kit-thank-you', 'thank-you'),
        dtt(r'^thank-you/tell-friend/?$', 'thank-you/tell-friend.html', 'contact-tell-friend', 'thank-you'),
        dtt(r'^thank-you/affiliate-enroll/?$', 'thank-you/affiliate-enroll.html', 'affiliate-enroll', 'thank-you'),


        url(r'^thank-you/(?P<custom_url>.*)/?$',
            'apps.common.views.thank_you', name='custom_thank_you',),
        
        # Landing Pages
            # Agent 2.0 Landing Page
                dtt(r'^affiliate/agent-two/?$', 'affiliates/agent-two/index.html', 'agent-two-lp'),
                url(r'^package-code/?$', 'apps.pricetable.views.package_code', name='package-code'),
            # Spanish
            dtt(r'^es/?$', 'spanish/index.html',
                'pa-spanish'),
            # Hawaii
            dtt(r'^hialarm/?$', 'affiliates/hialarm/fluid-index.html',
                'pa-hialarm'),
            # Get Smart Page
            dtt(r'^getsmart/?$', 'mobile/get-smart.html', 'getsmart', 'index', ctx={'agent_id': 'i10288'}),

            # CJ Page
            dtt(r'^cj/?$', 'affiliates/cj/index.html', 'cj', 'index', ctx={'agent_id': 'a10028'}),


        # Affiliate Resources 
        dtt(r'^affiliates/resources/?$', 'affiliates/resources.html', 'aff'),
        url(r'^affiliates/resources/get-started/?$', 'apps.affiliates.views.get_started_page', name='aff-get-started'),
        url(r'^affiliates/resources/logos/?$','apps.affiliates.views.logos_page' ,name='aff-logos'),
        url(r'^affiliates/resources/web-banners/?$', 'apps.affiliates.views.web_banners_page', name='aff-web-banners'),
        url(r'^affiliates/resources/collateral/?$', 'apps.affiliates.views.collateral_page', name='aff-collateral'),
        url(r'^affiliates/resources/products/?$', 'apps.affiliates.views.products_page', name='aff-products'),
        url(r'^affiliates/login/?$', 'apps.affiliates.views.aff_login', name='aff-login'),                
        url(r'^api/affiliate/?$', 'apps.affiliates.views.accept_affiliate'),

        url(r'^api/affiliate/(?P<affiliate_id>[A-Za-z0-9\_-]+)/get/?$',
            'apps.affiliates.views.get_affiliate_information'),


        url(r'^news/', include('apps.news.urls', namespace='news')),
        url(r'^sitemaps/', include('apps.pa-sitemaps.urls', namespace='sitemaps')),
        url(r'^crime-rate/', include('apps.crimedatamodels.urls', namespace='crime-rate')),
        url(r'^search/?$', 'apps.search.views.search', name='search'),
        url(r'^testimonials/', include('apps.testimonials.urls',
            namespace='testimonials')),

        # CRM urls
        url(r'^crm/', include('apps.crm.urls', namespace='crm')),
        # EMAIL URLS
        url(r'^email/', include('apps.emails.urls', namespace='emails')),

        # comments urls
        url(r'^comments/posted/?$', 'apps.crm.views.comment_posted',
            name='comments-comment-done'),
        (r'^comments/', include('django.contrib.comments.urls')),

        ('^radioshack/?$',
            RedirectView.as_view(url='http://radioshack.protectamerica.com/',permanent=True)), 
        ('^feedback/?$',
            RedirectView.as_view(url='/pa/contact',permanent=True)),
            

        # SEM Landing Pages
        #dtt(r'^home-security/for-less/?$', 'affiliates/sem-landing-page/ppc-landing.html', 'sem-landing', 'home'),
        #forward to homepage

        # SEO Local Pages
        url(r'^(?P<keyword>%s)/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)/(?P<state>[A-Za-z\-]+)/?$' % ('|'.join(LOCAL_KEYWORDS)),
            'apps.local.views.local_page_wrapper',
            name='local-page-keyword'),
        url(r'^(?P<keyword>%s)/(?P<state>[A-Za-z\-]+)/sitemap\.xml' % ('|'.join(LOCAL_KEYWORDS)),
            'apps.local.views.sitemap',
            name='local-page-sitemap-state'),
        url(r'^(?P<keyword>%s)/sitemap\.xml' % ('|'.join(LOCAL_KEYWORDS)),
            'apps.local.views.sitemap_state',
            name='local-page-sitemap'),
        url(r'^local-pages-sitemap-index\.xml', 'apps.local.views.sitemap_index',
            name='keyword-sitemap-index'),

        # SEO Content Pages
        dtt(r'^home-security-systems/?$', 'seo-pages/home-security-systems.html', 'seo-home-security-systems', 'about-us'),
        dtt(r'^alarm-systems/?$', 'seo-pages/alarm-systems.html', 'seo-alarm-systems', 'about-us'),
        dtt(r'^ge-home-security/?$', 'seo-pages/ge-home-security.html', 'seo-ge-home-security', 'about-us'),
        dtt(r'^ge-home-security-systems/?$', 'seo-pages/ge-home-security-systems.html', 'seo-ge-home-security-systems', 'about-us'),
        dtt(r'^home-alarm-systems/?$', 'seo-pages/home-alarm-system.html', 'seo-home-alarm-systems', 'about-us'),
        dtt(r'^security-systems/?$', 'seo-pages/security-systems.html', 'seo-security-systems', 'about-us'),
        dtt(r'^home-security-system/?$', 'seo-pages/home-security-system.html', 'seo-home-security-system', 'about-us'),
        dtt(r'^best-home-security-system/?$', 'seo-pages/best-home-security-system.html', 'seo-best-home-security-system', 'about-us'),
        dtt(r'^home-security-companies/?$', 'seo-pages/home-security-companies.html', 'seo-home-security-companies', 'about-us'),

        # PAID LANDING PAGES
        #dtt(r'^home-security/business-security-systems/?$', 'affiliates/ppc-business-package/index.html', 'paid-business-landing-page'),
        #Redirect to Business Page
        dtt(r'^home-security/free-home-security-system/?$', 'affiliates/ppc-adt-clone/index.html', 'paid-adt-copy-cat'),
        dtt(r'^adt-vs-protect-america-compare-and-save/?$', 'affiliates/adt-comparison-two/index.html', 'paid-adt-comparison-cat'),
        dtt(r'^frontpoint-vs-protect-america-compare-and-save/?$', 'affiliates/frontpoint-vs-protectamerica/index.html', 'frontpoint-vs-pa'),
        dtt(r'^diy/do-it-yourself-home-security-system/?$', 'affiliates/diy-landing-page/index.html', 'paid-diy-landing-page'),
        dtt(r'^national-crime-prevention/?$', 'affiliates/crime-prevention-month/index.html', 'crime-prevention-month'),
        dtt(r'^wireless-home-security/?$', 'affiliates/wireless/index.html', 'wireless-landing-page'),
        dtt(r'^protect-america-vs-comcast/?$', 'affiliates/comcast-vs-protectamerica/index.html', 'comcast-vs-protect-america'),
        dtt(r'^protect-america-vs-vivint/?$', 'affiliates/vivint-vs-protectamerica/index.html', 'vivint-vs-protect-america'),
        dtt(r'^adt-comparison/?$', 'affiliates/adt-comparison/index.html', 'adt-two'),


        dtt(r'^direct-mail/?$', 'affiliates/direct-mail/index.html', 'direct-mail'),

        # CRIME STOPPERS
        dtt(r'^CFLA/?$', 'affiliates/crime-stoppers-cf/losangeles.html', 'cf-la'),
        dtt(r'^CFCHICAGO/?$', 'affiliates/crime-stoppers-cf/chicago.html', 'cf-chicago'),
        dtt(r'^CFCLEVELAND/?$', 'affiliates/crime-stoppers-cf/cleveland.html', 'cf-cleveland'),
        dtt(r'^CFMIAMI/?$', 'affiliates/crime-stoppers-cf/miami.html', 'cf-miami'),


)

# redirect urls
urlpatterns += patterns('',
    ('^pa/two-way-monitoring/Home-Security-System-Monitoring/?$',
        RedirectView.as_view(url='/products/alarm-monitoring/landline',permanent=True)), 
    ('^pa/two-way-monitoring/?$',
        RedirectView.as_view(url='/products/alarm-monitoring/landline',permanent=True)),
    ('^pa/affiliates/?$',
        RedirectView.as_view(url='/contact/affiliate-program/',permanent=True)), 
    ('^pa/home-security-opportunities/home-security/?$',
        RedirectView.as_view(url='/contact/careers/',permanent=True)), 
    ('^pa/home-security-opportunities/?$',
        RedirectView.as_view(url='/contact/careers/',permanent=True)), 
    ('^pa/support/?$',
        RedirectView.as_view(url='/support/',permanent=True)), 
    ('^pa/about/?$',
        RedirectView.as_view(url='/pa/about/home-security-companies/',permanent=True)), 
    ('^pa/priv_p/?$',
        RedirectView.as_view(url='/help/privacy-policy/',permanent=True)),
    ('^pa/priv_p/protect-america/?$',
        RedirectView.as_view(url='/help/privacy-policy/',permanent=True)), 
    ('^pa/return-policy/Home-Security/?$',
        RedirectView.as_view(url='/help/return-policy/',permanent=True)), 
    ('^pa/do-not-call/?$',
        RedirectView.as_view(url='/help/do-not-call/',permanent=True)),
    ('^pa/site_map/?$',
        RedirectView.as_view(url='/sitemap/',permanent=True)), 
    ('^secretkeypad/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories/',permanent=True)),
    ('^pa/ge_simon_xt/?$',
        RedirectView.as_view(url='/products/security-equipment/control-panels/ge-simon-xt/',permanent=True)), 
    ('^pa/ge_simon_3/?$',
        RedirectView.as_view(url='/products/security-equipment/control-panels/ge-simon-3/',permanent=True)),
    ('^pa/learn/?$',
        RedirectView.as_view(url='/pa/learn/alarm-companies/',permanent=True)), 
    ('^pa/operation/?$',
        RedirectView.as_view(url='/support/operation/',permanent=True)), 
    ('^pa/advantage/?$',
        RedirectView.as_view(url='/security-advantage/',permanent=True)), 
    ('^pa/troubleshooting/?$',
        RedirectView.as_view(url='/support/troubleshooting/',permanent=True)),
    ('^pa/security_sensors/?$',
        RedirectView.as_view(url='/products/security-equipment/sensors/',permanent=True)),
    ('^pa/faq/?$',
        RedirectView.as_view(url='/support/faq/',permanent=True)), 
    ('^pa/install/?$',
        RedirectView.as_view(url='/support/installation/',permanent=True)), 
    ('^pa/equipment/?$',
        RedirectView.as_view(url='/pa/equipment/wireless-home-security-system/',permanent=True)),
    ('^pa/license/?$',
        RedirectView.as_view(url='/help/state-licenses/',permanent=True)), 
    ('^pa/profile/?$',
        RedirectView.as_view(url='/pa/profile/home-alarm-systems/',permanent=True)), 
    ('^pa/charities/?$',
        RedirectView.as_view(url='/pa/charities/america-protect/',permanent=True)), 
    ('^pa/how_it_works/?$',
        RedirectView.as_view(url='/pa/how_it_works/ge-security-systems/',permanent=True)), 
    ('^pa/warranty/?$',
        RedirectView.as_view(url='/help/warranty/',permanent=True)), 
    ('^pa/monitoring/?$',
        RedirectView.as_view(url='/pa/monitoring/security-system/',permanent=True)), 
    ('^pa/installv/?$',
        RedirectView.as_view(url='/support/installation/',permanent=True)), 
    ('^local-directory/?$',
        RedirectView.as_view(url='http://homesecuritysystems.protectamerica.com/',permanent=True)), 
    ('^pa/safer_at_home/?$',
        RedirectView.as_view(url='/pa/learn/alarm-companies/',permanent=True)), 
    ('^pa/products/?$',
        RedirectView.as_view(url='/shop/home-security-systems/',permanent=True)), 
    ('^pa/packages/alarms/?$',
        RedirectView.as_view(url='/shop/home-security-systems/',permanent=True)), 
    ('^careers.php$',
        RedirectView.as_view(url='/contact/careers/',permanent=True)), 
    ('^pa/map/?$',
        RedirectView.as_view(url='/contact/find-us/',permanent=True)), 
    ('^pa/careers/?$',
        RedirectView.as_view(url='/contact/careers/',permanent=True)), 
    ('^pa/packages/?$',
        RedirectView.as_view(url='/pa/packages/alarms/',permanent=True)), 
    ('^pa/mistakes/?$',
        RedirectView.as_view(url='/pa/learn/alarm-companies/',permanent=True)), 
    ('^pa/home_security_accessories/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories/',permanent=True)), 
    ('^pa/home_automation/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories/home-automation/',permanent=True)),
    ('^pa/copper/home-security-systems/?$',
        RedirectView.as_view(url='/shop/copper-package',permanent=True)),
    ('^pa/home_automation/home-automation-devices/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories/home-automation',permanent=True)), 
    ('^pa/advantage/adt-security/?$',
        RedirectView.as_view(url='/security-advantage',permanent=True)), 
    ('^pa/platinum/alarm-system/?$',
        RedirectView.as_view(url='/shop/platinum-package',permanent=True)), 
    ('^pa/gold/alarm-systems/?$',
        RedirectView.as_view(url='/shop/gold-package',permanent=True)), 
    ('^pa/silver/alarm/?$',
        RedirectView.as_view(url='/shop/silver-package',permanent=True)),
    ('^pa/bronze/security-systems/?$',
        RedirectView.as_view(url='/shop/bronze-package',permanent=True)), 
    ('^pa/existing-home-security-system/cellular-monitoring/?$',
        RedirectView.as_view(url='/products/existing-security-system',permanent=True)), 
    ('^pa/install/home-security-wireless/?$',
        RedirectView.as_view(url='/support/installation',permanent=True)), 
    ('^pa/ge_simon_xt/ge-simon-xt/?$',
        RedirectView.as_view(url='/products/security-equipment/control-panels/ge-simon-xt',permanent=True)),
    ('^pa/broadband-monitoring/Alarm-System-Without-Phone-Line/?$',
        RedirectView.as_view(url='/products/alarm-monitoring/broadband',permanent=True)), 
    ('^pa/landline-monitoring/Home-Security-Monitoring-Service/?$',
        RedirectView.as_view(url='/products/alarm-monitoring/landline',permanent=True)), 
    ('^pa/troubleshooting/protect-america/?$',
        RedirectView.as_view(url='/support/troubleshooting',permanent=True)), 
    ('^pa/home_security_accessories/home-security-accessories/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories',permanent=True)), 
    ('^pa/security_sensors/home-security-sensors/?$',
        RedirectView.as_view(url='/products/security-equipment/sensors',permanent=True)), 
    ('^pa/cellular-monitoring/Wireless-Home-Security/?$',
        RedirectView.as_view(url='/products/alarm-monitoring/cellular',permanent=True)), 
    ('^pa/simon-xt-touchscreen/ge-simon-xt-touchscreen/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories/touchscreen',permanent=True)),
    ('^pa/return-policy/?$',
        RedirectView.as_view(url='/help/return-policy/',permanent=True)),
    ('^pa/request-moving-kit/?$',
        RedirectView.as_view(url='/pa/request-moving-kit/security-moving-kit',permanent=True)), 
    ('^home-security/business-security-systems$',
        RedirectView.as_view(url='/home-security/business-security-systems/',permanent=True)), 
    ('^crimeprevention$',
        RedirectView.as_view(url='crimeprevention/',permanent=True)), 

    ('^crimeprevention/?$',
        RedirectView.as_view(url='/national-crime-prevention/?agent=i03248',permanent=True)),  
    #('^national-crime-prevention$',
    #    RedirectView.as_view(), {'url': '/national-crime-prevention/', 'permanent': True}),

    ('^livechat_iframe.php',
        RedirectView.as_view(url='/support',permanent=True)), 
    ('^pa/yard-sign/security-yard-sign',
        RedirectView.as_view(url='/products/security-equipment/accessories',permanent=True)), 
    ('^pa/x10-appliance-module/home-security-automation',
        RedirectView.as_view(url='/home-security-blog/tag/x10-home-automation',permanent=True)), 
    ('^pa/outdoor_lighting/alarms-home',
        RedirectView.as_view(url='/products/security-equipment/accessories',permanent=True)), 
    ('^pa/x10-powerhorn-siren/security-siren',
        RedirectView.as_view(url='/home-security-blog/alarm-systems/simon-xt-alarm-system-features_2285',permanent=True)), 
    ('^pa/operation/monitoring-security',
        RedirectView.as_view(url='/home-security-blog/home-security/how-to-remote-monitor-home-video-security-camera-2_1311',permanent=True)), 
    ('^pa/compare/home-security-comparison',
        RedirectView.as_view(url='/home-security-blog/home-security-systems-2/home-security-systems-comparison-3_2604',permanent=True)),
    ('^pa/carbon-monoxide-detector/carbon-monoxide-detector',
        RedirectView.as_view(url= '/home-security-blog/home-security/home-security-information/home-security-tips/carbon-monoxide-poisoning_2985',permanent=True)), 
    ('^pa/x10-socket-rocket/home-security-automation',
        RedirectView.as_view(url='/home-security-blog/tag/x10-home-automation',permanent=True)), 
    ('^pa/landscaping/alarms-home-security',
        RedirectView.as_view(url='/home-security-blog/home-security/home-security-information/best-home-security-diy-projects-and-quick-tips_148',permanent=True)), 
    ('^pa/low-temperature-sensor/low-temperature-sensor',
        RedirectView.as_view(url='/products/security-equipment/sensors',permanent=True)),
    ('^pa/safer_at_home/security',
        RedirectView.as_view(url='/news/article/keep-homes-safe-with-home-security-systems_1232',permanent=True)),
    ('^pa/glass_around/alarm-home-system',
        RedirectView.as_view(url='/home-security/business-security-systems/',permanent=True)), 
    ('^pa/license/protect-america-licenses',
        RedirectView.as_view(url='/help/state-licenses/',permanent=True)),
    ('^pa/motion-detector/motion-detector',
        RedirectView.as_view(url='/products/security-equipment/sensors',permanent=True)), 
    ('^pa/faq/alarm-company-monitoring',
        RedirectView.as_view(url='/support/faq',permanent=True)), 
    ('^pa/site_map/protect-america',
        RedirectView.as_view(url='/sitemap/')), 
    ('^pa/window-decal/security-window-sticker',
        RedirectView.as_view(url= '/products/security-equipment/accessories',permanent=True)),
    ('^pa/low-price-guarantee/GE-Security-System',
        RedirectView.as_view(url='/help/low-price-guarantee',permanent=True)), 
    ('^pa/map/protect-america',
        RedirectView.as_view(url='/contact/find-us',permanent=True)), 
    ('^pa/ge_simon_3/ge-simon-3',
        RedirectView.as_view(url='/products/security-equipment/control-panels/ge-simon-xt',permanent=True)), 
    ('^pa/secure_vacation/alarm-house',
        RedirectView.as_view(url='/news/article/consider-home-security-before-going-on-vacation_31',permanent=True)),
    ('^pa/smoke-detector/smoke-detector/',
        RedirectView.as_view(url='/products/security-equipment/sensors',permanent=True)), 
    ('^pa/products/ge-home-security',
        RedirectView.as_view(url='/pa/equipment/wireless-home-security-system',permanent=True)),
    ('^https:/www.protectamerica.com/pa/security-affiliate-enrollment/security',
        RedirectView.as_view(url='/contact/affiliate-program/',permanent=True)), 
    ('^pa/home_automation/home-automation-devices',
        RedirectView.as_view(url='/home-security-blog/tag/home-automation-devices',permanent=True)), 
    ('^pa/support/home-security-alarm-system',
        RedirectView.as_view(url='/pa/monitoring/security-system',permanent=True)), 
    ('^pa/warranty/monitoring-security-system',
        RedirectView.as_view(url='/help/warranty',permanent=True)), 
    ('^pa/talking-wireless-keypad/wireless-keypad',
        RedirectView.as_view(url='/products/security-equipment/accessories',permanent=True)), 
    ('^pa/solar-yard-sign-light/solar-yard-sign-light',
        RedirectView.as_view(url='/products/security-equipment/accessories/',permanent=True)), 
    ('^pa/careers/home-security-jobs',
        RedirectView.as_view(url= '/contact/careers',permanent=True)), 
    ('^pa/complete-home-security/',
        RedirectView.as_view(url='/complete-home-security',permanent=True)), 
    ('^pa/command-station/security-system',
        RedirectView.as_view(url='/products/security-equipment/control-panels/ge-simon-xt',permanent=True)), 
    ('^pa/medical-panic-pendant/medical-panic-pendant',
        RedirectView.as_view(url='/products/security-equipment/accessories/',permanent=True)), 
    ('^pa/neighborhood_watch/burglar-alarm',
        RedirectView.as_view(url='/news/article/serial-burglars-suspected-of-thefts-in-california-neighborhood_453',permanent=True)), 
    ('^pa/dept/protect-america',
        RedirectView.as_view(url='/contact/department-listing',permanent=True)), 
    ('^pa/glass-break-detector/glass-break-detector',
        RedirectView.as_view(url='/ge-simon-security-systems/wireless-business-security/business-package',permanent=True)),
    ('^pa/door-or-window-sensor/door-sensor',
        RedirectView.as_view(url='/products/security-equipment/sensors/door-window-sensor',permanent=True)),
    ('^pa/keychain-remote-control/security-keychain-remote',
        RedirectView.as_view(url='/products/security-equipment/accessories/',permanent=True)), 
    ('^pa/security-of-information/protect-america',
        RedirectView.as_view(url='/help/security-of-information',permanent=True)), 
    ('^pa/order_2/home-security-monitoring-system',
        RedirectView.as_view(url='/products/order-package',permanent=True)), 
    ('^pa/home_security_checklist/home-protection',
        RedirectView.as_view(url='/home-security-blog/home-security/vacation-safety-tips_1684',permanent=True)),
    ('^pa/secure_garage/brinks-home-security',
        RedirectView.as_view(url='/news/article/diy-tips-for-garage-security_1306',permanent=True)), 
    ('^pa/video-home/',
        RedirectView.as_view(url='/pa/wireless-security-camera/ip-security-cameras',permanent=True)),
    ('^pa/flood-sensor/flood-sensor',
        RedirectView.as_view(url='/products/security-equipment/sensors',permanent=True)), 
    ('^pa/x10-lamp-module/home-security-automation',
        RedirectView.as_view(url='/home-security-blog/tag/x10-home-automation',permanent=True)), 
    ('^pa/video-business/',
        RedirectView.as_view(url='/products/interactive-video/business-video-camera',permanent=True)),

    # direct mail
    ('^AA1/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10017',permanent=True)), 
    ('^AA2/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10019',permanent=True)), 
    ('^AA3/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10021',permanent=True)), 
    ('^AA4/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10023',permanent=True)), 
    ('^AA5/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10025',permanent=True)), 
    ('^AB1/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10027',permanent=True)),

    ('^aa1/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10017',permanent=True)), 
    ('^aa2/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10019',permanent=True)), 
    ('^aa3/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10021',permanent=True)), 
    ('^aa4/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10023',permanent=True)),
    ('^aa5/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10025',permanent=True)), 
    ('^ab1/?$',
        RedirectView.as_view(url='/direct-mail/?agent=a10027',permanent=True)), 
    ('^feedback/?$',
        RedirectView.as_view(url='/pa/feedback',permanent=True)), 
    ('^ceo/?$',
        RedirectView.as_view(url='/pa/feedback',permanent=True)),
    ('^familyofcompanies/?$',
        RedirectView.as_view(url='/?agent=a02332',permanent=True)), 
    ('^angies/?$',
        RedirectView.as_view(url= '/?agent=a03103',permanent=True)), 
    ('^homesecurity/?$',
        RedirectView.as_view(url='/?agent=gr banner',permanent=True)), 
    ('shop/home-security-systems/?$',
        RedirectView.as_view(url='/shop/',permanent=True)),
    ('ge-simon-security-systems/wireless-home-alarm/copper-package/?$',
        RedirectView.as_view(url='/shop/copper-package/',permanent=True)),
    ('ge-simon-security-systems/wireless-home-alarm/bronze-package/?$',
        RedirectView.as_view(url='/shop/bronze-package/',permanent=True)),
    ('ge-simon-security-systems/wireless-home-alarm/gold-package/?$',
        RedirectView.as_view(url='/shop/gold-package/',permanent=True)),
    ('ge-simon-security-systems/wireless-home-alarm/platinum-package/?$',
        RedirectView.as_view(url='/shop/platinum-package/',permanent=True)),
    ('ge-simon-security-systems/wireless-home-alarm/business-package/?$',
        RedirectView.as_view(url='/shop/business-package/',permanent=True)),
    ('products/existing-security-system/?$',
        RedirectView.as_view(url='/shop/existing-security-system/',permanent=True)),
    ('products/security-equipment/control-panels/ge-simon-xt/?$',
        RedirectView.as_view(url='/equipment/home-security/ge-simon-xt/',permanent=True)),
    ('products/security-equipment/control-panels/ge-simon-3/?$',
        RedirectView.as_view(url='/equipment/home-security/ge-simon-3/',permanent=True)),
    ('products/security-equipment/sensors/flood-sensor/?$',
        RedirectView.as_view(url='/equipment/life-safety/flood-sensor/',permanent=True)),
    ('products/security-equipment/sensors/door-window-sensor/?$',
        RedirectView.as_view(url='/equipment/home-security/door-window-sensor/',permanent=True)),
    ('products/security-equipment/accessories/?$',
        RedirectView.as_view(url='/products/security-equipment/accessories/',permanent=True)),
    ('products/security-equipment/accessories/touchscreen/?$',
        RedirectView.as_view(url='equipment/home-security/touchscreen/',permanent=True)),
    ('products/security-equipment/accessories/secret-keypad/?$',
        RedirectView.as_view(url='/equipment/home-security/secret-keypad/',permanent=True)),
    ('products/security-equipment/accessories/home-automation/?$',
        RedirectView.as_view(url='/equipment/home-automation/',permanent=True)),
    ('products/interactive-control/?$',
        RedirectView.as_view(url='/equipment/smart-connect-app/',permanent=True)),
    ('pa/monitoring/security-system/?$',
        RedirectView.as_view(url='/learn-about-security/monitoring/security-system/',permanent=True)),
    ('pa/about/home-security-companies/?$',
        RedirectView.as_view(url='learn-about-security/protect-america/',permanent=True)),

)

urlpatterns += patterns('',
    ('^(?P<agent_id>[A-Za-z0-9\_-]+)/?$',
        'apps.common.views.redirect_wrapper'),
)

urlpatterns += patterns('',
    (r'^sitemap\.xml', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    def adt(request, path):
        from django.views.generic.simple import direct_to_template
        return direct_to_template(request, path)
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}),

   )
