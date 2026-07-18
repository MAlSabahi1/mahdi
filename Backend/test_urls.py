import django
from django.urls import get_resolver

resolver = get_resolver()
for url in resolver.url_patterns:
    print(url)
