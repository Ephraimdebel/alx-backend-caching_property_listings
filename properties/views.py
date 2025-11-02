# from django.http import JsonResponse
# from django.views.decorators.cache import cache_page
# from .models import Property

# @cache_page(60 * 15)  # Cache for 15 minutes
# def property_list(request):
#     properties = Property.objects.all().values(
#         "id", "title", "description", "price", "location", "created_at"
#     )

#     return JsonResponse({
#         "data": list(properties)
#     })

from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # 15 minute view-level cache
def property_list(request):
    properties = get_all_properties()

    return JsonResponse({
        "data": properties
    })
