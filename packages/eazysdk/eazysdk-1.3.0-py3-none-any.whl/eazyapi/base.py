from __future__ import unicode_literals
from __future__ import absolute_import
from get import Get
from post import Post
from patch import Patch
from delete import Delete


class EazyAPI:
    """
    Creates a new instance of the EazyAPI
    """
    def __init__(self):
        self.get = Get()
        self.post = Post()
        self.patch = Patch()
        self.delete = Delete()
