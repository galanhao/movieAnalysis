from django.db.models import Q
from django.test import TestCase

# Create your tests here.
from proxyManager.models import Proxy


# class SimpleTest(TestCase):
#     def test_getHTML(self):
#         proxys = Proxy.objects.values("ip").filter(Q(https=1)|Q(https=1))
#         print(proxys)
#         return False


if __name__ == "__main__":
    proxys = Proxy.objects.values("ip").filter(Q(https=1) | Q(https=1))
    print(proxys)