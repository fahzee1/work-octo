from pricetable.models import Package

def price_table(request):
    # grab all the info on the specific packages and return them to the
    # request to be accessed

    price_dict = {}
    for package in Package.objects.all():
        price_dict[package.name] = package

    return {'pricetable': price_dict}
