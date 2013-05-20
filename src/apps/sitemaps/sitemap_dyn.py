import urls
import csv
import os.path
from django.conf import settings

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
'''
NOTE: there's some code here to allow for processing contexts 
from various types of url objects.  It's left in place, because it makes sense
to eventually handle a potential extra_context (or similar dict) for every type of url.
However, this would mean that every view on the site would need to be modified to expect such a dict...
not prepared to make such a sweeping change at this time
'''

URL_COLLECTION = {}


def read_site_CSV(csvFilePath='sitemap.csv', headerrow=0, keyCol=0):
    #os.path.abspath(path)
    csvDict = {}
    headerList = []
    keySequenceList = []
    csvFullFilePath = os.path.join(settings.PROJECT_ROOT, 'src', 'apps', 'sitemaps', csvFilePath)
    with open (csvFullFilePath, 'rb') as csvfile:
        site_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        rowcount = 0
        for row in site_reader:
            if(rowcount != headerrow):
                rowKey = row[keyCol]
                keySequenceList.append(rowKey)
                #print(rowKey + " : ))))))))))))((((((((((((" )
            for col in row:
                if(headerrow == rowcount):
                    headerList.append( col.strip() )
                else:
                    if( len(headerList) > -1 ):
                        idCol = headerList[keyCol]
                        csvDict[ rowKey ] = {}
                        for colNum in range(len(headerList) ):
                            header = headerList[colNum]
                            cellVal = row[colNum]
                            csvDict[ rowKey ][ header ] = cellVal
                    #else:
                        #currently depends on column name keys
                        #would need to create a generator for AI names
            rowcount += 1
    return csvDict, keySequenceList

def checkContext(u_dict, ctx, checklist="parent,page_name,linkText", verbose=False):
    for theKey in ctx:
        if( isDict(ctx[theKey]) ):
            theDict = ctx[theKey]
            loopDict(theDict)
        for theSelKey in checklist.split(","):
            if(theKey == theSelKey):
                ctxVal = ctx[theKey]
                u_dictVal = u_dict[theKey]
                if(ctxVal != None and ctxVal != ''):
                    u_dict[theKey] = ctx[theKey]
    return u_dict

def checkUStruct(u, Ucount=0):
    str_parent =  str(u['parent'])
    str_page_name =  str(u['page_name'])
    str_linkText =  str(u['linkText'])
    return u

def isDict(theVar):
    if( isinstance(theVar, dict) ):
        return True
    else:
        return False

def isTuple(theVar):
    if( isinstance(theVar, tuple) ):
        return True
    else:
        return False

def loopDict(theDict, tabs="", depth=0):
    tabs = tabs + "\t"
    depthlimit = 3
    for theKey in theDict:
        keyType = type(theKey).__name__
        if( keyType == 'str' ):
            valType = type(theDict[ theKey ]).__name__
            if( isDict( theDict[ theKey ] ) ):
                if(depth < depthlimit):
                    if( str(theKey).find("___") > -2 ):
                        loopDict(theDict[ theKey ], tabs=tabs, depth=depth+1)

def crawlEntry(Entry):
    tabs="\t\t"
    entryDict = Entry.__dict__
    theCrawlDict = entryDict
    if( isDict( theCrawlDict ) ):
        loopDict(theCrawlDict, tabs=tabs)
        theentryDict = Entry[theKey]
        for dKey in theentryDict:
            if( isDict(theentryDict[dKey]) ):
                loopDict(theentryDict[dKey], tabs=tabs)
def uStruct():
    tUStr = {
            'typ':'', 
            'parent': '', 
            'page_name':'', 
            'linkText' : '', 
            'url': '', 
            'trace' : '', 
            'show_me' : True
            }

    return tUStr
    
def index(request):
    site_CSV_Dict, site_CSV_Key_sequence_list = read_site_CSV()
    site_CSV_Dict_Chil, site_chil_CSV_Key_sequence_list = read_site_CSV(csvFilePath='sitemap_children.csv')
    site_CSV_Dict.update(site_CSV_Dict_Chil)
    site_CSV_Key_sequence_list = site_CSV_Key_sequence_list + site_chil_CSV_Key_sequence_list

    #for sql in site_CSV_Key_sequence_list:
    #    print(sql)
    #    if(sql == 'external-comparison' ):
    #        print('|||||||||||||||||||||||||||||||||||external-comparison' )
    #v1=v12931728743982374

    def sequenceDictList(theDict):
        #thisRootOrder123 = site_CSV_Key_sequence_list
        thisProduceList = []
        #print("ooooooooooooooooooooooooIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        #print("ooooooooooooooooooooooooIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        #print("ooooooooooooooooooooooooIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        for oi1 in site_CSV_Key_sequence_list:
            #print("oyoy: " + oi1)
            if(oi1 == "external-comparison"):
                v123 = 1
                #print("@@@!^&!&!@@@@@@@@@@@@@#@#@#@#@#@#@#@#@")
                #print("@@@!^&!&!@@@@@@@@@@@@@#@#@#@#@#@#@#@#@")
                #print("@@@!^&!&!@@@@@@@@@@@@@#@#@#@#@#@#@#@#@")
                #v1 = v7676767676
            #if(oi1.strip() == 'clear-my-cookies'):
                #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                #v1= v736847326483746583746
            if(oi1 not in theDict.keys() ):
                v123 = 1
                #print("remove: " + oi1)
                #print( "typeeeee:  " + type(thisRootOrder123).__name__ )
                #thisRootOrder123.remove(oi1)
            else:
                #print("===============================================: " + oi1)
                thisProduceList.append(oi1)
        
        #V1 = V87687403985093485
        #print("INNER SEQUENCE CHECK@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #for unc in site_CSV_Key_sequence_list:
            #print("+_+_+_+_+_+_*^*^*^*^" + unc)
        #print("END INNER SEQUENCE CHECK@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return thisProduceList

    def id_url(entry, passParent, count=0):
        u = uStruct()

        if( 'default_args' in dir(entry) ):
            u['typ'] = "url?"
            if('extra_context' in entry.default_args):
                u['typ'] = "dtt_ext"
                u = checkContext(u, entry.default_args['extra_context'])
                u = checkContext(u, entry.default_args, verbose=False)
            else:
                u = checkContext(u, entry.default_args, verbose=False)
                if( not len(u['page_name']) ):
                    if( type(entry.name).__name__ == "str" ):
                        if( len(entry.name) ):
                            u['page_name'] = entry.name
        
        if( len( u['page_name'] ) >0 ):
                try:
                    u['url'] = reverse(u['page_name'])
                except:
                    x1 = 123
        return checkUStruct(u, count)

    p_d = {}
    p_d['sitemap-comparison'] = ['paid-adt-copy-cat', 'comcast-vs-protect-america', 'vivint-vs-protect-america']

    def generateSiteMap():
        rootOrder = ['products', 'contact-us', 'find-us', 'order-package', 'index', 'clear-my-cookies', 'sky', 'home', 'thank_you', 'keyword-sitemap-index', 'paid-business-landing-page', 'paid-adt-copy-cat', 'paid-adt-comparison-cat', 'frontpoint-vs-pa', 'paid-diy-landing-page', 'crime-prevention-month', 'wireless-landing-page', 'comcast-vs-protect-america', 'vivint-vs-protect-america', 'adt-two', 'direct-mail', 'cf-la', 'cf-chicago', 'cf-cleveland', 'cf-miami', 'payitforward', 'payitforward-point-tracking', 'about-us', 'family', 'testimonials', 'video-testimonials', 'send-testimonial', 'tell-a-friend', 'complete-home-security', 'contact-us', 'affiliate-program', 'feedback-ceo', 'help', 'do-not-call', 'support', 'moving-kit', 'package-code', 'aff', 'search', 'comments-comment-done']
        hideList = ['keyword-sitemap-index']

    def valParser(theVal):
        if( theVal != None ):
            if( type(theVal).__name__ == "str" ):
                if(theVal.strip() == ""):
                    return None
                else:
                    return theVal.strip()
            else:
                return theVal
        else:
            return None

    def keyStrParser(theDict, theKey, trace=""):
        '''
            if isdefined keyDict['url'
            if dict has key
            if val type is string
            if string has length
                if len( str() )
        '''
        retStr = ""
        if(theKey in theDict):
            if( type(theDict[theKey]).__name__ == "str" ):
                retStr = theDict[theKey]
                retStr = retStr.strip()
        return retStr

    def updateColl(key, keyDict, source):
        '''
            - check for existence of key
            - if none, generate using function
            - populate where appropriate 

        '''
        print("UC:key=[" + key + "]")
        if key in URL_COLLECTION:
            #here
            '''
                make sure all keys exist
            '''
            print("====UC use:" + key)
            us = uStruct()
            for test in us:
                '''
                    looping over possible keys
                '''
                if(test in URL_COLLECTION[key] ):
                    x1 = 1 
                    #print(key + " : " + test + ' key exists: not set********************************************')
                else:
                    #set defaults
                    URL_COLLECTION[key][test] = us[test]
                    #print(test + ' set*********************************************')
        else:
            #not here
            #print("{{{{UC make:" + key)
            URL_COLLECTION[key] = uStruct()
        #print("-----------------------------------------------------------------------")
        #print("source: " + source)

        
        if(source == "site"):
            '''
                use url
                if isdefined keyDict['url'
                if dict has key
                if val type is string
                if string has length
                    if len( str() )


            
            urlStr = keyStrParser(keyDict, 'url')
            if( len(urlStr) > 0):
                URL_COLLECTION[key] = urlStr
            '''
            #for kley in keyDict:
                #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + kley + ": " + str(keyDict[kley]) )
            subkey = 'url'
            keyStr = keyStrParser(keyDict, subkey, trace="site")
            #print("ks: " + keyStr)
            if( len(keyStr) > 0):
                URL_COLLECTION[key][subkey] = keyStr
                #print("keySTR: ===================================================")
            #else:
            #    print("keySTR: ___________________________________________________" + str(keyDict) ) 

            
        elif(source == "csv"):
            '''
                use parent, linkText, show_me
                valParser(theVal)
            '''
            subkey = 'parent'
            keyStr = keyStrParser(keyDict, subkey, trace="csv")
            if( len(keyStr) > 0):
                URL_COLLECTION[key][subkey] = keyStr

            subkey = 'linkText'
            keyStr = keyStrParser(keyDict, subkey, trace="csv2")
            if( len(keyStr) > 0):
                URL_COLLECTION[key][subkey] = keyStr

            subkey = 'show_me'
            keyStr = keyStrParser(keyDict, subkey, trace="csv3")
            if( len(keyStr) > 0):
                URL_COLLECTION[key][subkey] = keyStr

        #print("-----------------------------------------------------------------------")

    def foldSiteDicts(uDict1, uDict2, parent):
        '''
            ud1 is site-based
            ud2 is csv-based
            
            URL_COLLECTION replaces uDict3

        '''
        uDict3 = {}
        
        for ud2_key in uDict2.keys():
            #looping over csv keys
            #is there a link matching this item?
            #print("--------------")
            

            '''
                1. set trace string for source of update
                2. 
                    uStruct()

                'typ':'', 
                'parent': '', 
                'page_name':'', 
                'linkText' : '', 
                'url': '', 
                'trace' : ''
                'show_me' : ''
            '''

            ud2 = uDict2[ud2_key]

            theSource = "csv"
            #print("&&&&&&&&&&&&&&&&&&&&&&&")
            #for u2k in uDict2[ud2_key]:
            #    print(u2k)
            updateColl(ud2_key, uDict2[ud2_key], theSource)
            continue

            try:
                hasUd2Key = False
                if( ud2_key in uDict3.keys() ):
                    ud1 = uDict3[ud2_key]
                    hasUd2Key = True
                    ud1['trace'] += ' [ud2loop :if]'
                    #print("from 3:[" + ud2_key+ "] found")
                elif(ud2_key in uDict1.keys() ):
                    #print("from 2:[" + ud2_key+ "] found")
                    ud1 = uDict1[ud2_key]
                    ud1['trace'] += ' [ud2loop :elif]'
                else:
                    ud1 = uStruct()
                    ud1['trace'] += ' [ud2loop :else]'  
                if( hasUd2Key ):
                    #actually get ud1 from uDict3, if it exists?  
                    #maybe?  from previous processing ^^^^^^^^^^^^
                    ud1Parent = str(ud1["parent"]).strip()
                    ud2Parent = str(ud2["parent"]).strip()
                    if(ud1Parent != ud2Parent):
                        #print("||||||||||||||||||||||||diff, yo... u1 be like all [" + ud1Parent + "], but u2 be like all [" + ud2Parent +"] interesting and less structured")
                        #what we do?
                        
                        if(ud2["parent"]==parent):
                            ud1["parent"] = ud2["parent"]                                                                                                                             
                            uDict3[ud2_key] = ud1
                            #if(ud2_key == "payitforward-involved"):
                            #    print("ALERT!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2" +  str(ud2["parent"]) + ':trace:' + str(ud2["trace"]))
                #else:
                    
                    #print("missing from ...narrowed site list...match to passed parent..")
                    #if(ud2['parent'].strip() == parent):
                    #    print("OMGOMGOMGOMG__________________________________________________________________________")
                    #but what precedence?
                    #ultimate authority here is csv, so ultimate is ud2
                    #...compare ud2_parent with passed parent 
                    #print(ud2_key )
                    #print("\tsite:" + str(ud1['parent']) )
                    #print("\t csv:" + str(ud2['parent']) )
            except Exception, err:
                #print("nooooooooooooooooos:" + str( type(err).__name__ ) + ": " + "; ".join(err))
                pass

        for ud1_key in uDict1.keys():

            theSource = "site"
            #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            #for ik in uDict1[ud1_key]:
            #    print( ik + ":=)" + str(uDict1[ud1_key][ik]) )
            updateColl(ud1_key, uDict1[ud1_key], theSource)
            continue

            #if(ud1_key == "payitforward-involved"):
            #    print("")
            #    print("")
            #    print("")
            #    print("============================================123========")
            ##    print("============================================123========")
            #    print("============================================123========")

            #looping over site keys
            #transfer link Text from csv to sitelist
            ud1 = uDict1[ud1_key]
            #if 'trace' in ud1:
            #    print("trace is here")
            #else:
            #    print("trace is n't here")
            #    ud1['trace'] = '[created in ud1 key loop]'

            try:
                ud2 = uDict2[ud1_key]
            #    print("|per|" + str(ud2["parent"]) + "||")
                if(parent==ud2["parent"]):
            #        print("like UD2")
                    ud1["parent"] = ud2["parent"]
                    ud1['trace'] += '[ud1 if:1]'
                if(ud1_key == "payitforward-involved"):
            #        print("u2_1:" + str(ud1["parent"]) + ":2:" + str(ud2["parent"]))
                    ud1['trace'] += '[ud1 if:2]'
                #if(ud1["parent"] != ud2["parent"]):
                #    ud1["parent"] = ud2["parent"]
                    #need to handle this in drill-down, because by this point, it's too late
            #        print("u2_1:" + str(ud1["parent"]) + ":2:" + str(ud2["parent"]))
                if(len(ud2["linkText"].strip())):
                    ud1['trace'] += '[ud1 if:3]'
                    ud1["linkText"] = ud2["linkText"]
                    #do any more assignments before setting
                    #check to see if show_me flag is false
                    '''
                    maybe loop through all of 2 and see if there's one that matches parent 
                    and not in 1
                    does this mean the 2 loop should happen 1st?
                    '''
                    if(ud2["show_me"].upper().strip() == "FALSE"):
                        v123 = 1
                        ud1['trace'] += '[ud1 if:4]'
                    else:
                        if(ud1["parent"] == parent):
                            ud1['trace'] += '[ud1 if:5]'
            #                print("+++++++++++" + str(ud1_key) + " [" + str(ud1["parent"]) + "][" + str(parent) +"]")
                            #if(ud1_key == "payitforward-involved"):
                            #    print("ALERT!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@1" + ':trace:' + str(ud1["trace"]))
                            #    print("")
                            #    print("")
                            #    print("")
                            #    return uDict3
                            uDict3[ud1_key] = ud1
            except Exception, err:
                #print("exception{{" + ud1_key  + "}}-"+ "; ".join(err))
                uDict3[ud1_key] = ud1
                pass
        return uDict3

    def sortUDict(uDict, pageString='', parent=None, rec=0):
        ND = narrowUDict(uDict, parent)
        NDO = site_CSV_Dict
        #for xkey in NDO.keys():
        #    print(NDO[xkey]["page_name"]  )

        ND = foldSiteDicts(ND, NDO, parent)
        '''
            ^^^ might be able to bypass some of this now
            URL_COLLECTION
            need to alert when URL_COLLECTION subkeys are set...so far empty at end
        '''

        pageString+=  "<table border=1>"
        for collKey in URL_COLLECTION:
            hasURL = False
            hasLink = False
            pageString += "<tr>"
            pageString+= "<td>"
            pageString+= collKey
            pageString+= "</td>"

            if( isDict(URL_COLLECTION[collKey]) ):
                #pageString+= "is dict<br />"
                if('url' in URL_COLLECTION[collKey]):
                    v1=1
                    #pageString+= "has url<br />"
                    #pageString+= URL_COLLECTION[collKey]['url'] + "<br />"

                    #if( len( keyStrParser(URL_COLLECTION[collKey], 'url', trace="readout:  url3232") )  ):
                        #hasURL = True
            else:
                pageString+= collKey + ": not dict<br />"

            if( hasURL ):
                
                pageString+= "<td>"
                pageString+= URL_COLLECTION[collKey]['url'] 
                pageString+= "</td>"



                #pageString+= "==============+++++++++++++--------------<br />"
                #pageString+="==============+++++++++++++--------------<br />"
                #pageString+= "url: " + URL_COLLECTION[collKey]['url'] + "<br />"
                #pageString+= "not dict<br />"
            pageString += "</tr>"
        pageString+=  "</table>" 
        return pageString

        #for nnd in ND.keys():
        #    print(nnd)

        if(len(ND) > 0):
            pageString += "<ul>"
            rootlist = []

            ND_Start_keys = ND.keys()
            rootOrder = site_CSV_Key_sequence_list

            for oi in rootOrder:
                if(oi not in ND.keys() ):
                    rootOrder.remove(oi)
            ND_Ordered_Keys = rootOrder

            for thisU_key in ND_Ordered_Keys:
                if thisU_key not in ND.keys():
                    continue
                thisU = ND[ thisU_key ]

                pageString += "<li"
                if(parent != None):
                    pageString += " class='child'"
                pageString += ">"
                pageString += "<a href='" + thisU['url'] + "'>"
                thisTrace = ""
                if 'trace' in thisU:
                    thisTrace = thisU['trace']
                pageString += thisU['linkText'] + ": [" + thisU['page_name'] + "]<br />trace["  + thisTrace + "]" 
                pageString += "</a>"
                rootlist.append(thisU['page_name'])
                cND = narrowUDict(uDict, parent=thisU['page_name'])
                if( len( cND ) ):
                    pageString += "<ul>"
                    for cND_item_key in cND:
                        cND_item = cND[cND_item_key]
                        cND2 = narrowUDict(uDict, parent=cND_item['page_name'] )
                        pageString += "<li"
                        pageString += " class='child'"
                        pageString += ">"
                        pageString += "<a href='" + cND_item['url'] + "'>"
                        pageString +=  cND_item['linkText'] + ": [" + cND_item['page_name'] + "]"
                        pageString += "</a>"
                        pageString += "</li>"
                        if( len( cND2 ) ):
                            pageString += "<ul>"
                            for cND2_item_key in cND2:
                                cND2_item = cND2[cND2_item_key]
                                cND3 = narrowUDict(uDict, parent=cND2_item['page_name'] )
                                pageString += "<li"
                                pageString += " class='child'"
                                pageString += ">"
                                pageString += "<a href='" + cND2_item['url'] + "'>"
                                pageString +=  cND2_item['linkText']
                                pageString += "</a>"
                                pageString += "</li>"
                            pageString += "</ul>"
                    pageString += "</ul>"
                pageString += "</li>"  
            pageString += "</ul>"
            #pageString += str(rootlist)
        return pageString

    def narrowUList(uList, parent):
        uOne = []
        uDict = {}
        for u2 in uList:  
            if( u2['parent'] == ''):
                u2['parent'] = None
            if(parent == u2['parent']):
                if( len(u2['url']) ):
                    if(u2['linkText'] == ''):
                        u2['linkText'] = u2['page_name'].replace('-', ' ').capitalize()
                    uOne.append(u2) 
                    if( len( u2['page_name'] ) ):
                        uDict[ u2['page_name'] ] = u2
        return uOne

    def narrowUDict(uDict_in, parent):
        uDict = {}
        for _u in uDict_in:
            u2 = uDict_in[_u]
            print("++")
            if( str(u2['parent']).strip() == ''):
                u2['parent'] = None
            if( str(u2['parent']).strip() == 'None'):
                u2['parent'] = None

            for pd_key in p_d:
                if(u2['page_name'] in p_d[pd_key]):
                    u2['parent'] = pd_key

            if( (parent == u2['parent'])):
                if( len(u2['url']) ):
                    if(u2['linkText'] == ''):
                        u2['linkText'] = u2['page_name'].replace('-', ' ').capitalize()
                    if( len( u2['page_name'] ) ):
                        uDict[ u2['page_name'] ] = u2
        return uDict

    def narrowUDict1(uDict_in, parent):
        uDict = {}
        for _u in uDict_in:
            u2 = uDict_in[_u]
            #if _u.strip() == "clear-my-cookies":
                #print("===================================++++++++++++++++++++++++++++++++ cookiecrisp")

            #print("++parent++" + str(u2["parent"])  +  "\tshow_me:" + str(u2["show_me"])  + ":" + type(u2["show_me"]).__name__)
            if( str(u2["parent"]).strip() == str(parent).strip() ):
                if( str(u2["show_me"]).strip() == 'True'):



                    #if(_u == "external-comparison"):
                
                    #    if( str(parent) == 'None'):
                    #        print("|||||||||||||||\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\  parent: " + _u)



                    #if _u.strip() == "clear-my-cookies":
                    #    print("|||||||||||||||||||||||||||||||||||||||||||||||||||++++++++++++++++++++++++++++++++ cookiecrisp")
                    u2["page_name"] = _u
                    #print("++parent++" + str(u2["parent"]) + ":page_name:" + str(u2["page_name"]) +";"+ _u + "\tshow_me:" + str(u2["show_me"]) + ":" + type(u2["show_me"]).__name__ )
                    #print("   ++page_name:" + str(u2["page_name"]) )
                    #print("   ++=" + str(u2["linkText"]) )
                    uDict[u2['page_name']] = u2
        return uDict

    def sort_urls(urllist, parent=None, tabstring="\t"):
        count = 0
        pages = ''
        newcount = 0

        uList = []
        uDict = {}
        for entry in urllist:
            count+=1
            U_Item = id_url(entry, parent, count)
            if U_Item["page_name"] in uDict:
                for uKey in uDict[ U_Item["page_name"] ]:
                    #looping through output dict
                    #compare | uDict[ U_Item["page_name"] ] : U_Item
                    if( uDict[ U_Item["page_name"] ][uKey] !=  U_Item[ uKey ]):
                        #if the values don't match:  merge:
                        if(uDict[ U_Item["page_name"] ][uKey] == ''):
                            uDict[ U_Item["page_name"] ][uKey] = U_Item[ uKey ]
                        if(uDict[ U_Item["page_name"] ][uKey] == None):
                            uDict[ U_Item["page_name"] ][uKey] = U_Item[ uKey ]
            else:
                uDict[ U_Item["page_name"] ] = U_Item
            uList.append( U_Item )

        '''
        



        '''
        siteDict = uDict
        csvDict = site_CSV_Dict
        noMeaningfulReturn = foldSiteDicts(siteDict, csvDict, parent)

        #for sItem in siteDict:
            #print(sItem + " ============================================))))))))))))))")
            #if( sItem.find("viv") > -1 ):
                #if(sItem in URL_COLLECTION):
                #    print("ahoy")
                #else:
                 #   print("arrrr")
                #print(")()()()(================================================++++++++++++++++++++++++++++++++++++++++")
        #v1 = v87678964583475893475


        #pages = sortUDict(URL_COLLECTION)
        pages = ""
        pages2=""
        rootDict = narrowUDict1(URL_COLLECTION, None)

        pages2 += "<ul>"
        ucount =0

        '''
            the item 'external-comparison' 
                is in rootDict, 
                but
                is not in 
                thisRootSeq
            find the csv loop .. identify where the url evaluation
        '''

        thisRootSeq = sequenceDictList(rootDict)

        #for uuc2 in site_CSV_Key_sequence_list:
           # print("|||" + uuc2)
            #if(uuc2.find("floo") > -1):
                #print("|||||||||||||||||||||||||||||||||||||")
        #v1234 = w098098


        for uuc in thisRootSeq:
            ucount += 1
            #print( str(ucount) + ":" + uuc + "!!" + str( rootDict[uuc]['show_me'] ))
            pages2 += "<li>"
            if( len( rootDict[uuc]['url'].strip() ) ):
                pages2 += "<a href='" + rootDict[uuc]['url'] + "'>" 
            if( len(rootDict[uuc]['linkText']) ):
                pages2 += rootDict[uuc]['linkText'] 
            else:
                pages2 += uuc
            if( len( rootDict[uuc]['url'].strip() ) ):
                pages2 += "</a>" 
            lvl2Dict = narrowUDict1(URL_COLLECTION, uuc)

            if( len(lvl2Dict) ):
                thisLvl2Seq = sequenceDictList(lvl2Dict)
                pages2 += "<ul>"
                for lvl2 in thisLvl2Seq:
                    lvl2D = lvl2Dict[lvl2]
                    pages2 += "<li class='child'>"
                    if( len( lvl2Dict[lvl2]['url'].strip() ) ):
                        pages2 += "<a href='" + lvl2Dict[lvl2]['url'] + "'>" 
                    if( len(lvl2Dict[lvl2]['linkText']) ):
                        pages2 += lvl2D['linkText']
                    else:
                        pages2 += lvl2
                    if( len( lvl2Dict[lvl2]['url'].strip() ) ):
                        pages2 += "</a>"
                    lvl3Dict = narrowUDict1(URL_COLLECTION, lvl2)

                    if( len(lvl3Dict) ):
                        thisLvl3Seq = sequenceDictList(lvl3Dict)
                        pages2 += "<ul>"
                        for lvl3 in thisLvl3Seq:
                            lvl3D = lvl3Dict[lvl3]
                            pages2 += "<li class='child'>"
                            if( len( lvl3Dict[lvl3]['url'].strip() ) ):
                                pages2 += "<a href='" + lvl3Dict[lvl3]['url'] + "'>" 
                            if( len(lvl3Dict[lvl3]['linkText']) ):
                                pages2 += lvl3D['linkText']
                            else:
                                pages2 += lvl3
                            if( len( lvl3Dict[lvl3]['url'].strip() ) ):
                                pages2 += "</a>"

                            lvl4Dict = narrowUDict1(URL_COLLECTION, lvl3)
                            if( len(lvl4Dict) ):
                                thisLvl4Seq = sequenceDictList(lvl4Dict)
                                pages2 += "<ul>"
                                for lvl4 in lvl4Dict:
                                    lvl4D = lvl4Dict[lvl4]
                                    pages2 += "<li class='child'>"
                                    pages2 += "<a href='" + lvl4Dict[lvl4]['url'] + "'>" 
                                    pages2 += lvl4D['linkText']
                                    pages2 += "</a>" 
                                    pages2 += "</li>"
                                pages2 += "</ul>"
                            pages2 += "</li>"
                        pages2 += "</ul>"
                    pages2 += "</li>"
                pages2 += "</ul>"

            pages2 += "</li>"
        pages2 += "</ul>"
        pages2 += "<hr />"
        pages2 += "<hr />"

        pages = pages2 + pages
        #print("rd2d")
        #for rD in rootDict:
        #    print("rd: " + rD)

        if count > 0:
            return '<ul>' + pages + '</ul>'
        return pages
    pages = sort_urls(urls.urlpatterns)

    return render_to_response('sitemaps/sitemap.html', {'pages':pages},
                              context_instance=RequestContext(request))
