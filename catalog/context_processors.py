from .models import Version, Product


def active_version(request):
    active_versions = {}
    products = Product.objects.all()
    for product in products:
        active_version = product.version_set.filter(is_active=True).first()
        if active_version:
            active_versions[product.id] = active_version.version_name
    return {'active_versions': active_versions}
