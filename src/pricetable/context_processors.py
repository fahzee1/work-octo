from pricetable.models import Package

def price_table(request):
    # grab all the info on the specific packages and return them to the
    # request to be accessed
    
    def return_none_if_zero(value):
        if value == '0':
            return None
        else:
            return '$%s' % value

    price_dict = {}
    for package in Package.objects.all():
        info_dict = {
            'name': package.name,
            'upfront': return_none_if_zero(package.upfront),
            'adt_upfront':return_none_if_zero(package.adt_upfront),
            'standard_monitoring':return_none_if_zero(package.standard_monitoring),
            'landline_monitoring':return_none_if_zero(package.landline_monitoring),
            'broadband_monitoring':return_none_if_zero(package.broadband_monitoring),
            'cellular_monitoring':return_none_if_zero(package.cellular_monitoring),
            'cellular_interactive_monitoring':return_none_if_zero(package.cellular_interactive_monitoring),
        }
        price_dict[package.name] = info_dict

    return {'pricetable': price_dict}
