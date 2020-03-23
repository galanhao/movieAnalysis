from django.test import TestCase

# Create your tests here.

from proxyManager.tasks import testWriteFile, clearIP


def test_testWriteFile():
    print("S")
    testWriteFile.delay()

def test_clearIP():
    clearIP().delay()
test_clearIP()