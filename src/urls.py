from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.views.decorators.cache import cache_page
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

urlpatterns = patterns('',
    # Example:
    # (r'^protectamerica/', include('protectamerica.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls'))

    # Uncomment the next line to enable the admin:
    # Custom Admin Url
    (r'^django-admin/affiliates/affiliate/add/$',
        'apps.affiliates.views.add_affiliate'),
    (r'^django-admin/affiliates/affiliate/(?P<affiliate_id>\d+)/$',
        'apps.affiliates.views.edit_affiliate'),
    (r'^django-admin/', include(admin.site.urls)),

    #contact us
    url(r'^contact/ajaxpost/?$', 'apps.contact.views.ajax_post'),
    url(r'^contact-us/?$', 'apps.contact.views.main', name='contact-us'),
    
    url(r'^contact-us/find-us/?$', 'apps.contact.views.find_us', name='find-us'),
    url(r'^products/order-package/?$', 'apps.contact.views.order_form',
        name='order-package'),
    url(r'^sitemap.xml$', 'django.views.generic.simple.direct_to_template', {
            'template': 'sitemaps/index.xml',
            'mimetype': 'application/xml',
        }, name='index'),
    url(r'^sitemap/', include('apps.pa-sitemaps.urls', namespace='sitemaps')),
    url(r'^support/clear-my-cookies/$', 'apps.common.views.clear_my_cookies',
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
        dtt(r'^$', 'affiliates/radioshack/_base.html', 'home', ctx={'page_name': 'index', 'agent_id': 'a02596'}),
        dtt(r'^thank-you/$', 'affiliates/radioshack/thank-you.html', 'thankyou', ctx={'page_name': 'thankyou', 'agent_id': 'a02596'}),
        dtt(r'^cswitch/$', 'affiliates/radioshack/content_switch.html', 'cswitch', ctx={'page_name': 'index', 'agent_id': 'a02596'}),

    )
# Paid landing site
elif settings.SITE_ID == 3:
    urlpatterns += patterns('',
        url(r'^$', 'apps.affiliates.views.semlanding_home'),
        url(r'^google/?$', 'apps.affiliates.views.semlanding_google'),
        url(r'^grbanner/?$', 'apps.affiliates.views.semlanding_google'),
        url(r'^msn/?$', 'apps.affiliates.views.semlanding_bing'),
        dtt(r'^test/touchscreen/$', 'affiliates/sem-landing-page/test/touchscreen-banner-test.html', 'touchscreen-test'),
        dtt(r'^business/$', 'affiliates/ppc-business-package/index.html', 'paid-business-landing-page'),
        dtt(r'^test/equip/$', 'affiliates/sem-landing-page/test/equipment-included.html', 'bbb-test-B'),
        dtt(r'^test/exp/$', 'affiliates/sem-landing-page/test/adds-expiration.html', 'bbb-test-C'),

    )
elif settings.SITE_ID == 4:
    urlpatterns += patterns('',
        # local pages
        url(r'^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)/$', 'apps.local.views.local_page',
            name='local-page'),
        url(r'^(?P<state>[A-Z]{2})/$', 'apps.local.views.local_city',
            name='choose-city'), 
        url(r'^(?P<keyword>%s)/sitemap\.xml', 'apps.local.views.sitemap',
            name='keyword-sitemap'),
        url(r'^$', 'apps.local.views.local_state', name='local-state'),
# 301 perm redirect from / to non-/ on article pages
        ('^(?P<state>[A-Z]{2})/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)$',
            redirect_to, {'url': '/%(state)s/%(city)s/', 'permanent': True}),
    )
elif settings.SITE_ID == 5:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/all-the-things/base.html', 'home', ctx={'page_name': 'index', 'agent_id': 'AllTheThings'}),
    )
# 5 Linx landing site
elif settings.SITE_ID == 6:
    urlpatterns += patterns('',
        dtt(r'^$', 'affiliates/five-linx/index.html', 'home', ctx={
            'agent_id': 'a01526'}),

        dtt(r'^copper$', 'affiliates/five-linx/copper.html', 'copper', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^makes-sense$', 'affiliates/five-linx/makes-sense.html', 'makes-sense', 'home', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^bronze$', 'affiliates/five-linx/bronze.html', 'bronze', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^silver$', 'affiliates/five-linx/silver.html', 'silver', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^gold$', 'affiliates/five-linx/gold.html', 'gold', 'security-packages', ctx={
            'agent_id': 'a01526'}),
        dtt(r'^platinum$', 'affiliates/five-linx/platinum.html', 'platinum', 'security-packages', ctx={
            'agent_id': 'a01526'}),

        dtt(r'^video$', 'affiliates/five-linx/video.html', 'video', ctx={
            'agent_id': 'a01526'}),

        dtt(r'^gps$', 'affiliates/five-linx/gps.html', 'gps', ctx={
            'agent_id': 'a01526'}),
        
        dtt(r'^order$', 'affiliates/five-linx/order.html', 'order', ctx={
            'agent_id': 'a01526'}),
            
        dtt(r'^thank-you/5linx/$', 'affiliates/five-linx/thank-you.html', 'thank-you', ctx={
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
            
        dtt(r'^thank-you/tomboy-tools/$', 'affiliates/tomboy-tools/thank-you.html', 'thank-you', ctx={
            'agent_id': 'a03169'}),


    )
# Mobile Website
elif settings.SITE_ID == 9:
    urlpatterns += patterns('',
        url(r'^$', 'apps.pricetable.views.index', name='home'),
        url(r'^home-security-packages/$', 'apps.pricetable.views.packages', name='packages'),
        url(r'^security-add-ons/$', 'apps.pricetable.views.adds', name='add-ons'),
        url(r'^home-security/$', 'apps.pricetable.views.home_security', name='home-security'),
        url(r'^home-security-monitoring/$', 'apps.pricetable.views.monitoring', name='monitoring'),
        url(r'^interactive-monitoring-features/$', 'apps.pricetable.views.interactive', name='interactive'),
        url(r'^customer-info/$', 'apps.pricetable.views.customer_info', name='customer-info'),

        url(r'^request-quote/$', 'apps.pricetable.views.quote', name='get-quote'),
        url(r'^cart/$', 'apps.pricetable.views.mobile_cart', name='cart'),
        url(r'^add-to-cart/$', 'apps.pricetable.views.add_to_cart', name='add_to_cart'),
        url(r'^remove-from-cart/$', 'apps.pricetable.views.remove_from_cart', name='remove_from_cart'),
        url(r'^cart-checkout/$', 'apps.pricetable.views.mobile_cart_checkout', name='cart-checkout'),
    )
# Black Friday Site
elif settings.SITE_ID == 10:
    urlpatterns += patterns('',

        url(r'^$', 'apps.common.views.black_friday', name='index'),

    )
elif settings.SITE_ID == 11:
    urlpatterns += patterns('',
        dtt(r'^$', 'external/get-a-home-security-system/index.html', 'home'),
    )
else:
    urlpatterns += patterns('',

        # Test Pages
        dtt(r'^test/tcr-first/$', 'tests/top-consumer-test.html', 'tcr-first-test', 'home'),
        dtt(r'^test/promotion-first/$', 'tests/promotion-tcr-banner-test.html', 'promotion-first-test', 'home'),
        url(r'^test/index/(?P<test_name>[a-zA-Z\_\-]+)/$', 'apps.common.views.index_test', name='index_test'),

        # Home Page
        url(r'^$', 'apps.common.views.index', name='home'),
        url(r'^thank-you/?$', 'apps.common.views.thank_you',
            name='thank_you'),
            
        # SEO Local Pages
        url(r'^(?P<keyword>%s)/(?P<city>[a-zA-Z\-\_0-9\s+\(\),\'\.]+)/(?P<state>[A-Za-z\-]+)/(?P<zipcode>\d+)/$' % ('|'.join(LOCAL_KEYWORDS)),
            'apps.local.views.local_page_wrapper',
            name='local-page-keyword'),
        url(r'^(?P<keyword>%s)/sitemap\.xml' % ('|'.join(LOCAL_KEYWORDS)),
            'apps.local.views.sitemap',
            name='local-page-sitemap'),
        url(r'^local-pages-sitemap-index\.xml', 'apps.local.views.sitemap_index',
            name='keyword-sitemap-index'),

        # SEO Content Pages
        dtt(r'^home-security-systems/$', 'seo-pages/home-security-systems.html', 'seo-home-security-systems', 'about-us'),
        dtt(r'^alarm-systems/$', 'seo-pages/alarm-systems.html', 'seo-alarm-systems', 'about-us'),
        dtt(r'^ge-home-security/$', 'seo-pages/ge-home-security.html', 'seo-ge-home-security', 'about-us'),
        dtt(r'^ge-home-security-systems/$', 'seo-pages/ge-home-security-systems.html', 'seo-ge-home-security-systems', 'about-us'),
        dtt(r'^home-alarm-systems/$', 'seo-pages/home-alarm-system.html', 'seo-home-alarm-systems', 'about-us'),
        dtt(r'^security-systems/$', 'seo-pages/security-systems.html', 'seo-security-systems', 'about-us'),
        dtt(r'^home-security-system/$', 'seo-pages/home-security-system.html', 'seo-home-security-system', 'about-us'),
        dtt(r'^best-home-security-system/$', 'seo-pages/best-home-security-system.html', 'seo-best-home-security-system', 'about-us'),
        dtt(r'^home-security-companies/$', 'seo-pages/home-security-companies.html', 'seo-home-security-companies', 'about-us'),

        # PAID LANDING PAGES
        dtt(r'^home-security/business-security-systems/$', 'affiliates/ppc-business-package/index.html', 'paid-business-landing-page'),
        dtt(r'^home-security/free-home-security-system/$', 'affiliates/ppc-adt-clone/index.html', 'paid-adt-copy-cat'),
        dtt(r'^adt-vs-protect-america-compare-and-save/$', 'affiliates/adt-comparison/index.html', 'paid-adt-comparison-cat'),
        dtt(r'^frontpoint-vs-protect-america-compare-and-save/$', 'affiliates/frontpoint-comparison/index.html', 'paid-adt-comparison-cat'),
        dtt(r'^diy/do-it-yourself-home-security-system/$', 'affiliates/diy-landing-page/index.html', 'paid-diy-landing-page'),
        dtt(r'^national-crime-prevention/$', 'affiliates/crime-prevention-month/index.html', 'crime-prevention-month'),
        dtt(r'^wireless-home-security/$', 'affiliates/wireless/index.html', 'wireless-landing-page'),
        dtt(r'^protect-america-vs-comcast/$', 'affiliates/comcast-vs-protectamerica/index.html', 'comcast-vs-protect-america'),

        dtt(r'^direct-mail/$', 'affiliates/direct-mail/index.html', 'direct-mail'),

        # CRIME STOPPERS        
        dtt(r'^CFLA/$', 'affiliates/crime-stoppers-cf/losangeles.html', 'cf-la'),
        dtt(r'^CFCHICAGO/$', 'affiliates/crime-stoppers-cf/chicago.html', 'cf-chicago'),
        dtt(r'^CFCLEVELAND/$', 'affiliates/crime-stoppers-cf/cleveland.html', 'cf-cleveland'),
        dtt(r'^CFMIAMI/$', 'affiliates/crime-stoppers-cf/miami.html', 'cf-miami'),

        # Thank You Pages
        dtt(r'^thank-you/contact-us/?$', 'thank-you/contact-us.html', 'contact-thank-you', 'thank-you'),
        dtt(r'^thank-you/ceo/?$', 'thank-you/ceo-thank-you.html', 'ceo-thank-you', 'thank-you'),
        dtt(r'^thank-you/moving-kit/?$', 'thank-you/moving-kit.html', 'moving-kit-thank-you', 'thank-you'),
        dtt(r'^thank-you/tell-friend/?$', 'thank-you/tell-friend.html', 'contact-tell-friend', 'thank-you'),
        dtt(r'^thank-you/affiliate-enroll/?$', 'thank-you/affiliate-enroll.html', 'affiliate-enroll', 'thank-you'),

        # CJ Page
        dtt(r'^cj/?$', 'affiliates/cj/index.html', 'cj', 'index', ctx={'agent_id': 'a10028'}),
        
        url(r'^thank-you/(?P<custom_url>.*)/?$',
            'apps.common.views.thank_you', name='custom_thank_you',),

        # pay it forward page
        dtt(r'^payitforward/$', 'payitforward/payitforward.html',
            'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/about/$', 'payitforward/about.html',
            'payitforward-about', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/press/$', 'payitforward/press.html',
            'payitforward-press', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/extras/$', 'payitforward/extras.html',
            'payitforward-extras', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/rules/$', 'payitforward/rules.html',
            'payitforward-rules', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/thankyou/$', 'payitforward/thankyou.html', 
            'payitforward-thankyou', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/teams/$', 'payitforward/teams.html',
            'payitforward-teams', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/teams/2012/spring/$', 'payitforward/spring2012.html',
            'payitforward-spring2012', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/teams/2012/fall/$', 'payitforward/fall2012.html',
            'payitforward-fall2012', 'payitforward', ctx={'agent_id': 'i03237'}),
        #dtt(r'^payitforward/involved/?$', 'payitforward/involved.html',
        #    'payitforward-involved', 'payitforward', ctx={'agent_id': 'i03237'}),
        url(r'^payitforward/involved/$',
            'apps.contact.views.payitforward', name='payitforward-involved'),
        #dtt(r'^payitforward/point-tracking/$', 'payitforward/point-tracking.html',
        #    'payitforward-point-tracking', 'payitforward', ctx={'agent_id': 'i03237'}),
        url(r'^payitforward/point-tracking/$', 'apps.payitforward.views.point_tracking',
            name='payitforward-point-tracking'),
        dtt(r'^payitforward/awareness/$', 'payitforward/awareness.html',
            'payitforward-awareness', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/point-scale/$', 'payitforward/point-scale.html',
            'payitforward-point-scale', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/revenue/$', 'payitforward/revenue.html',
            'payitforward-revenue', 'payitforward', ctx={'agent_id': 'i03237'}),
        dtt(r'^payitforward/video/$', 'payitforward/video.html',
            'payitforward-video', 'payitforward', ctx={'agent_id': 'i03237'}),
            dtt(r'^payitforward/press/$', 'payitforward/press.html',
            'payitforward-press', 'payitforward', ctx={'agent_id': 'i03237'}),

        # Product > Advantage

        dtt(r'^security-advantage/?$', 'products/advantage.html', 'advantage', 'products'),

        # Home Security Packages
        dtt(r'^pa/packages/alarms/?$', 'packages/index.html', 'products'),

            # Product > Packages

            dtt(r'^ge-simon-security-systems/wireless-home-alarm/copper-package/?$', 'packages/copper.html', 'copper', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/bronze-package/?$', 'packages/bronze.html', 'bronze', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/silver-package/?$', 'packages/silver.html', 'silver', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/gold-package/?$', 'packages/gold.html', 'gold', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-home-alarm/platinum-package/?$', 'packages/platinum.html', 'platinum', 'products'),
            dtt(r'^ge-simon-security-systems/wireless-business-security/business-package/?$', 'packages/business.html', 'business', 'products'),

            # Product > Monitoring

            dtt(r'^pa/monitoring/security-system/?$', 'products/monitoring/index.html', 'monitoring', 'products'),

                dtt(r'^products/alarm-monitoring/landline/?$', 'products/monitoring/landline.html', 'landline', 'monitoring'),
                dtt(r'^products/alarm-monitoring/broadband/?$', 'products/monitoring/broadband.html', 'broadband', 'monitoring'),
                dtt(r'^products/alarm-monitoring/cellular/?$', 'products/monitoring/cellular.html', 'cellular', 'monitoring'),

            # Product > Equipment

            dtt(r'^pa/equipment/wireless-home-security-system/?$', 'products/equipment/index.html', 'equipment', 'products'),

                        #dtt(r'^products/security-equipment/control-panels/?$', 'products/equipment/control-panels.html', 'control-panel', 'equipment'),
                            dtt(r'^products/security-equipment/control-panels/ge-simon-xt/?$', 'products/equipment/simon-xt.html', 'simon-xt', 'control-panel'),
                            dtt(r'^products/security-equipment/control-panels/ge-simon-3/?$', 'products/equipment/simon-3.html', 'simon-3', 'control-panel'),


                        # Product > Equipment > Security Sensors

                        dtt(r'^products/security-equipment/sensors/?$', 'products/equipment/security-sensors.html', 'sensors', 'equipment'),
                            dtt(r'^products/security-equipment/sensors/flood-sensor/?$', 'products/equipment/flood-sensor.html', 'flood-sensor', 'sensors'),
                            dtt(r'^products/security-equipment/sensors/door-window-sensor/?$', 'products/equipment/door-window-sensor.html', 'door-window-sensor', 'sensors'),
                        
                        # Product > Equipment > Accessories
                        dtt(r'^products/security-equipment/accessories/?$', 'products/equipment/security-accessories.html', 'accessories', 'equipment'),
                            dtt(r'^products/security-equipment/accessories/touchscreen/?$', 'products/equipment/touchscreen.html', 'touchscreen', 'accessories'),
                            dtt(r'^products/security-equipment/accessories/secret-keypad/?$', 'products/equipment/secret-keypad.html', 'secret-keypad', 'accessories'),
                            #dtt(r'^products/security-equipment/accessories/home-automation/?$', 'products/equipment/home-automation.html', 'home-automation', 'accessories'),

            # Product > Video

            dtt(r'^pa/wireless-security-camera/ip-security-cameras/?$', 'products/video/index.html', 'video', 'products'),

                # Product > Video > Home
                dtt(r'^products/interactive-video/home-video-cameras?$', 'products/video/video-home.html', 'video-home', 'video'),

                # Product > Video > Business
                dtt(r'^products/interactive-video/business-video-cameras?$', 'products/video/video-business.html', 'video-business', 'video'),

            # Product > GPS Vehicle Tracking

            dtt(r'^pa/vehicle-gps-tracking/gps-services/?$', 'products/gps/index.html', 'gps', 'products'),

            # Product > Cell Takeover

            dtt(r'^products/existing-security-system/?$', 'products/cell-takeover/index.html', 'cell-takeover', 'products'),
            
            # Product > Interactive Control

            dtt(r'^products/interactive-control/?$', 'products/interactive/index.html', 'interactive-control', 'products'),

        # About Pages

        dtt(r'^pa/about/home-security-companies/?$', 'about-us/index.html', 'about-us'),

            # About > Profile

            dtt(r'^pa/profile/home-alarm-systems/?$', 'about-us/profile.html', 'profile', 'about-us'),

            # About > Family of Companies

            #dtt(r'^pa/family-of-companies/america-protect/?$', 'about-us/family-of-companies.html', 'family', 'about-us'),
            url(r'^pa/family-of-companies/america-protect/?$',
                'apps.common.views.family_of_companies',
                name='family'),

            # About > Charities

            dtt(r'^pa/charities/america-protect/?$', 'about-us/charities.html', 'charities', 'about-us'),
            
            # About > How it Works

            dtt(r'^pa/how_it_works/ge-security-systems/?$', 'about-us/how-it-works.html', 'how-it-works', 'about-us'),

            # About > Learn About Security

            dtt(r'^pa/learn/alarm-companies/?$', 'about-us/learn-about-security.html', 'learn-about-security', 'about-us'),


            #dtt(r'^pa/testimonials/?$', 'about-us/testimonials.html', 'testimonials', 'about-us'),
            url(r'^pa/testimonials/?$',
                'apps.testimonials.views.view_testimonials',
                name='testimonials'),
            url(r'^video-testimonials/?$',
                'apps.testimonials.views.view_vidimonials',
                name='video-testimonials'),
                
                url(r'^video-testimonials/(?P<testimonial_id>\d+)/?$',
                    'apps.testimonials.views.vidimonial', 
                    name='single-video-testimonial'),
                #dtt(r'^pa/share-your-testimonial/?$', 'about-us/send-testimonial.html', 'send-testimonial', 'testimonials'),
                url(r'^pa/share-your-testimonial/?$',
                    'apps.testimonials.views.send_testimonial', 
                    name='send-testimonial'),



            # About > Tell a Friend

            #dtt(r'^about-us/tell-a-friend/?$', 'about-us/tell-a-friend.html', 'tell-a-friend', 'about-us'),
            url(r'^pa/cust_ref/?$',
                'apps.contact.views.tell_a_friend', 
                name='tell-a-friend'),

        
        # Complete Home Security 
        
        dtt(r'^complete-home-security/?$', 'complete-home-security/index.html', 'complete-home-security'),
        
        # Contact Pages

        #dtt(r'^contact-us/?$', 'contact-us/index.html', 'contact-us'),
        url(r'^pa/contact/?$', 'apps.contact.views.main',
            name='contact-us'),

        
            # Contact Pages > Find Us
            dtt(r'^contact/find-us/?$', 'contact-us/find-us.html', 'find-us', 'contact-us'),
            
            # Contact Pages > Department Listing
            dtt(r'^contact/department-listing/?$', 'contact-us/department-listing.html', 'department-listing', 'contact-us'),

            # Contact Pages > Affiliate Program
            #dtt(r'^contact/affiliate-program/?$', 'contact-us/affiliates.html', 'affiliate-program', 'contact-us'),
            url(r'^contact/affiliate-program/$',
                'apps.affiliates.views.signup', name='affiliate-program'),
            
            # Contact Pages > Careers
            dtt(r'^contact/careers/?$', 'contact-us/careers.html', 'careers', 'contact-us'),

            # Contact Pages > Feedback to CEO
            #dtt(r'^contact/send-thad-a-message/?$', 'contact-us/feedback-ceo.html', 'feedback-ceo', 'contact-us'),
            url(r'^pa/feedback/?$', 'apps.contact.views.ceo',
                name='feedback-ceo'),



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

        # Support Pages
        
        dtt(r'^support/?$', 'support/index.html', 'support'),

            # Support Pages > Installation
                dtt(r'^support/installation/?$', 'support/installation.html', 'installation', 'support'),
            # Support Pages > Operation
                dtt(r'^support/operation/?$', 'support/operation.html', 'operation', 'support'),
            # Support Pages > Troubleshooting
                dtt(r'^support/troubleshooting/?$', 'support/troubleshooting.html', 'troubleshooting', 'support'),
            # Support Pages > FAQs
                dtt(r'^support/faq/?$', 'support/faq.html', 'faq', 'support'),
            # Support Pages > Moving Kit
                #dtt(r'^support/moving-kit/?$', 'support/moving-kit.html', 'moving-kit', 'support'),
                url(r'^pa/request-moving-kit/security-moving-kit/?$',
                    'apps.contact.views.moving_kit', name='moving-kit'),
                url(r'^package-code/$',
                    'apps.pricetable.views.package_code', name='package-code'),
        
        # Affiliate Resources
        
        dtt(r'^affiliate/resources/?$', 'affiliates/resources.html', 'aff'),
        url(r'^api/affiliate/$', 'apps.affiliates.views.accept_affiliate'),

        url(r'^api/affiliate/(?P<affiliate_id>[A-Za-z0-9\_-]+)/get/$',
            'apps.affiliates.views.get_affiliate_information'),

    url(r'^news/', include('apps.news.urls', namespace='news')),
    url(r'^sitemaps/', include('apps.pa-sitemaps.urls', namespace='sitemaps')),
    url(r'^crime-rate/', include('apps.crimedatamodels.urls', namespace='crime-rate')),
    url(r'^search/$', 'apps.search.views.search', name='search'),
    url(r'^testimonials/', include('apps.testimonials.urls',
        namespace='testimonials')),
    # CRM urls
    url(r'^crm/', include('apps.crm.urls', namespace='crm')),
    # EMAIL URLS
    url(r'^email/', include('apps.emails.urls', namespace='emails')),

    # comments urls
    url(r'^comments/posted/$', 'apps.crm.views.comment_posted',
        name='comments-comment-done'),
    (r'^comments/', include('django.contrib.comments.urls')),

    ('^radioshack/?$',
        redirect_to, {'url': '/?agent=a02596', 'permanent': True}),
    ('^feedback/?$',
        redirect_to, {'url': '/pa/contact', 'permanent': True}),

)
# redirect urls
urlpatterns += patterns('',
    ('^pa/two-way-monitoring/Home-Security-System-Monitoring/?$',
        redirect_to, {'url': '/products/alarm-monitoring/landline', 'permanent': True}),
    ('^pa/two-way-monitoring/?$',
        redirect_to, {'url': '/products/alarm-monitoring/landline', 'permanent': True}),
    ('^pa/affiliates/?$',
        redirect_to, {'url': '/contact/affiliate-program/', 'permanent': True}),
    ('^pa/home-security-opportunities/home-security/?$',
        redirect_to, {'url': '/contact/careers/', 'permanent': True}),
    ('^pa/home-security-opportunities/?$',
        redirect_to, {'url': '/contact/careers/', 'permanent': True}),
    ('^pa/support/?$',
        redirect_to, {'url': '/support/', 'permanent': True}),
    ('^pa/about/?$',
        redirect_to, {'url': '/pa/about/home-security-companies/', 'permanent': True}),
    ('^pa/priv_p/?$',
        redirect_to, {'url': '/help/privacy-policy/', 'permanent': True}),
    ('^pa/priv_p/protect-america/?$',
        redirect_to, {'url': '/help/privacy-policy/', 'permanent': True}),
    ('^pa/return-policy/Home-Security/?$',
        redirect_to, {'url': '/help/return-policy/', 'permanent': True}),
    ('^pa/do-not-call/?$',
        redirect_to, {'url': '/help/do-not-call/', 'permanent': True}),
    ('^pa/site_map/?$',
        redirect_to, {'url': '/sitemap/', 'permanent': True}),
    ('^secretkeypad/?$',
        redirect_to, {'url': '/products/security-equipment/accessories/', 'permanent': True}),
    ('^pa/ge_simon_xt/?$',
        redirect_to, {'url': '/products/security-equipment/control-panels/ge-simon-xt/', 'permanent': True}),
    ('^pa/ge_simon_3/?$',
        redirect_to, {'url': '/products/security-equipment/control-panels/ge-simon-3/', 'permanent': True}),
    ('^pa/learn/?$',
        redirect_to, {'url': '/pa/learn/alarm-companies/', 'permanent': True}),
    ('^pa/operation/?$',
        redirect_to, {'url': '/support/operation/', 'permanent': True}),
    ('^pa/advantage/?$',
        redirect_to, {'url': '/security-advantage/', 'permanent': True}),
    ('^pa/troubleshooting/?$',
        redirect_to, {'url': '/support/troubleshooting/', 'permanent': True}),
    ('^pa/security_sensors/?$',
        redirect_to, {'url': '/products/security-equipment/sensors/', 'permanent': True}),
    ('^pa/faq/?$',
        redirect_to, {'url': '/support/faq/', 'permanent': True}),
    ('^pa/install/?$',
        redirect_to, {'url': '/support/installation/', 'permanent': True}),
    ('^pa/equipment/?$',
        redirect_to, {'url': '/pa/equipment/wireless-home-security-system/', 'permanent': True}),
    ('^pa/license/?$',
        redirect_to, {'url': '/help/state-licenses/', 'permanent': True}),
    ('^pa/profile/?$',
        redirect_to, {'url': '/pa/profile/home-alarm-systems/', 'permanent': True}),
    ('^pa/charities/?$',
        redirect_to, {'url': '/pa/charities/america-protect/', 'permanent': True}),
    ('^pa/how_it_works/?$',
        redirect_to, {'url': '/pa/how_it_works/ge-security-systems/', 'permanent': True}),
    ('^pa/warranty/?$',
        redirect_to, {'url': '/help/warranty/', 'permanent': True}),
    ('^pa/monitoring/?$',
        redirect_to, {'url': '/pa/monitoring/security-system/', 'permanent': True}),
    ('^pa/installv/?$',
        redirect_to, {'url': '/support/installation/', 'permanent': True}),
    ('^local-directory/?$',
        redirect_to, {'url': 'http://homesecuritysystems.protectamerica.com/', 'permanent': True}),
    ('^pa/safer_at_home/?$',
        redirect_to, {'url': '/pa/learn/alarm-companies/', 'permanent': True}),
    ('^pa/products/?$',
        redirect_to, {'url': '/pa/packages/alarms/', 'permanent': True}),
    ('^careers.php$',
        redirect_to, {'url': '/contact/careers/', 'permanent': True}),
    ('^pa/map/?$',
        redirect_to, {'url': '/contact/find-us/', 'permanent': True}),
    ('^pa/careers/?$',
        redirect_to, {'url': '/contact/careers/', 'permanent': True}),
    ('^pa/packages/?$',
        redirect_to, {'url': '/pa/packages/alarms/', 'permanent': True}),
    ('^pa/mistakes/?$',
        redirect_to, {'url': '/pa/learn/alarm-companies/', 'permanent': True}),
    ('^pa/home_security_accessories/?$',
        redirect_to, {'url': '/products/security-equipment/accessories/', 'permanent': True}),
    ('^pa/home_automation/?$',
        redirect_to, {'url': '/products/security-equipment/accessories/home-automation/', 'permanent': True}),
    ('^pa/copper/home-security-systems/?$',
        redirect_to, {'url': '/ge-simon-security-systems/wireless-home-alarm/copper-package', 'permanent': True}),
    ('^pa/home_automation/home-automation-devices/?$',
        redirect_to, {'url': '/products/security-equipment/accessories/home-automation', 'permanent': True}),
    ('^pa/advantage/adt-security/?$',
        redirect_to, {'url': '/security-advantage', 'permanent': True}),
    ('^pa/platinum/alarm-system/?$',
        redirect_to, {'url': '/ge-simon-security-systems/wireless-home-alarm/platinum-package', 'permanent': True}),
    ('^pa/gold/alarm-systems/?$',
        redirect_to, {'url': '/ge-simon-security-systems/wireless-home-alarm/gold-package', 'permanent': True}),
    ('^pa/silver/alarm/?$',
        redirect_to, {'url': '/ge-simon-security-systems/wireless-home-alarm/silver-package', 'permanent': True}),
    ('^pa/bronze/security-systems/?$',
        redirect_to, {'url': '/ge-simon-security-systems/wireless-home-alarm/bronze-package', 'permanent': True}),
    ('^pa/existing-home-security-system/cellular-monitoring/?$',
        redirect_to, {'url': '/products/existing-security-system', 'permanent': True}),
    ('^pa/install/home-security-wireless/?$',
        redirect_to, {'url': '/support/installation', 'permanent': True}),
    ('^pa/ge_simon_xt/ge-simon-xt/?$',
        redirect_to, {'url': '/products/security-equipment/control-panels/ge-simon-xt', 'permanent': True}),
    ('^pa/broadband-monitoring/Alarm-System-Without-Phone-Line/?$',
        redirect_to, {'url': '/products/alarm-monitoring/broadband', 'permanent': True}),
    ('^pa/landline-monitoring/Home-Security-Monitoring-Service/?$',
        redirect_to, {'url': '/products/alarm-monitoring/landline', 'permanent': True}),
    ('^pa/troubleshooting/protect-america/?$',
        redirect_to, {'url': '/support/troubleshooting', 'permanent': True}),
    ('^pa/home_security_accessories/home-security-accessories/?$',
        redirect_to, {'url': '/products/security-equipment/accessories', 'permanent': True}),
    ('^pa/security_sensors/home-security-sensors/?$',
        redirect_to, {'url': '/products/security-equipment/sensors', 'permanent': True}),
    ('^pa/cellular-monitoring/Wireless-Home-Security/?$',
        redirect_to, {'url': '/products/alarm-monitoring/cellular', 'permanent': True}),
    ('^pa/simon-xt-touchscreen/ge-simon-xt-touchscreen/?$',
        redirect_to, {'url': '/products/security-equipment/accessories/touchscreen', 'permanent': True}),
    ('^pa/return-policy/?$',
        redirect_to, {'url': '/help/return-policy/', 'permanent': True}),
    ('^pa/request-moving-kit/?$',
        redirect_to, {'url': '/pa/request-moving-kit/security-moving-kit', 'permanent': True}),
    ('^home-security/business-security-systems$',
        redirect_to, {'url': '/home-security/business-security-systems/', 'permanent': True}),
    ('^crimeprevention$',
        redirect_to, {'url': 'crimeprevention/', 'permanent': True}),
   
    ('^crimeprevention/$',
        redirect_to, {'url': '/national-crime-prevention/?agent=i03248', 'permanent': True}),
    #('^national-crime-prevention$',
    #    redirect_to, {'url': '/national-crime-prevention/', 'permanent': True}),
    # direct mail
    ('^AA1/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10017', 'permanent': True}),
    ('^AA2/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10019', 'permanent': True}),
    ('^AA3/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10021', 'permanent': True}),
    ('^AA4/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10023', 'permanent': True}),
    ('^AA5/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10025', 'permanent': True}),
    ('^AB1/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10027', 'permanent': True}),

    ('^aa1/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10017', 'permanent': True}),
    ('^aa2/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10019', 'permanent': True}),
    ('^aa3/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10021', 'permanent': True}),
    ('^aa4/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10023', 'permanent': True}),
    ('^aa5/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10025', 'permanent': True}),
    ('^ab1/?$',
        redirect_to, {'url': '/direct-mail/?agent=a10027', 'permanent': True}),
    ('^feedback/?$',
        redirect_to, {'url': '/pa/feedback', 'permanent': True}),
    ('^ceo/?$',
        redirect_to, {'url': '/pa/feedback', 'permanent': True}),
    ('^familyofcompanies/?$',
        redirect_to, {'url': '/?agent=a02332', 'permanent': True}),
)
urlpatterns += patterns('',
    ('^(?P<agent_id>[A-Za-z0-9\_-]+)/?$',
            'apps.common.views.redirect_wrapper'),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns() 
    def template_view(request, path):
        from django.views.generic.simple import direct_to_template
        return direct_to_template(request, path)
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^templates/(?P<path>.*)$', template_view),
   )
