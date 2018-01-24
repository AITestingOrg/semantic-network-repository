from celery import Celery


class OnlyOne:
    class __OnlyOne:
        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne(arg)

    def __getattr__(self, name):
        return getattr(self.instance, name)


app = Celery('tasks', broker='pyamqp://guest@localhost//')
