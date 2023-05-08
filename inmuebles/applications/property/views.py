# from django.shortcuts import render
# from .models import Property
# from django.http import JsonResponse

# def property_list(request):
#     properties = Property.objects.all()
#     data = {
#         'inmuebles' : list(properties.values())
#     }
#     return JsonResponse(data)

# def property_detail(request, pk):
#     properties = Property.objects.get(pk = pk)
#     data = {
#         'address' : properties.address,
#         'pais' : properties.country,
#         'image' : properties.image.url,
#         'active' : properties.active,
#         'description' : properties.description
#     }
#     return JsonResponse(data)
