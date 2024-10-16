# htmlwriter.py - part of qplot docs
# (C) Daniel Wagenaar 2024

"""This is a quaint little html writer that abuses Pythons "with"
construct to make sure tags are closed.

See below for an example.

Key usage note: There can only be one Html object at a time.

with Html() as h:
  with Head():
    with Title():
      h.write("Hello world")
"""


_text = None
_count = 0


def _add(txt):
    global _text
    _testopen()
    _text += txt
    

def _properties(**kwargs):
    if len(kwargs) == 0:
        return ""
    res = ""
    for k, v in kwargs.items():
        if k=="class_" or k=="type_":
            res += f" {k[:-1]}="
        else:
            res += f" {k}="
        res += f'"{v}"'
    return res


def _testopen():
    global _count
    if _count < 1:
        raise Exception("No Html object is open")
    elif _count > 1:
        raise Exception("There can only be one Html object at a time")


def tag(name, **properties):
    '''An opening tag or a tag that will not be closed'''
    global _text
    _testopen()
    _text += f"<{name}"
    _text += _properties(**properties)
    _text += ">"
    

class Tag:
    '''A tag with content, i.e., <tag>content</tag>'''
    def __init__(self, name, **properties):
        self.name = name
        self.props = properties

    def __enter__(self):
        tag(self.name, **self.props)
        return self

    def __exit__(self, *args):
        global _text
        _testopen()
        _text += f"</{self.name}>"
    
    

class _ETag(Tag):
    def __init__(self, name, **properties):
        super().__init__(name, **properties)
        
    def __exit__(self, *args):
        super().__exit__(*args)
        _add("\n")


class _SETag(Tag):
    def __init__(self, name, **properties):
        super().__init__(name, **properties)
    def __enter__(self):
        super().__enter__()
        _add("\n")
        return self
    
    def __exit__(self, *args):
        super().__exit__(*args)
        _add("\n")


class Html(_SETag):
    def __init__(self, **properties):
        super().__init__("html", **properties)
        global _text
        global _count        
        if _count != 0:
            raise Exception("There can only be one Html object at a time")
        _count += 1
        _text = "<!DOCTYPE html>\n"

    def __enter(self):
        super().__enter__()
        _add("\n")
        return self

    def __exit(self, *args):
        super().__exit__(*args)
        global _count
        if _count != 1:
            raise Exception("There can only be one Html object at a time")
        _count -= 1  

    def __iadd__(self, txt):
        _add(txt)
        return self

    
class Head(_SETag):
    def __init__(self, **properties):
        super().__init__("head", **properties)

        
class Title(_ETag):
    def __init__(self, **properties):
        super().__init__("title", **properties)

        
class Body(_SETag):
    def __init__(self, **properties):
        super().__init__("body", **properties)


class H1(_ETag):
    def __init__(self, **properties):
        super().__init__("h1", **properties)


class H2(_ETag):
    def __init__(self, **properties):
        super().__init__("h2", **properties)


class H3(_ETag):
    def __init__(self, **properties):
        super().__init__("h3", **properties)


class H4(_ETag):
    def __init__(self, **properties):
        super().__init__("h4", **properties)


class P(_SETag):
    def __init__(self, **properties):
        super().__init__("p", **properties)


class Div(_SETag):
    def __init__(self, **properties):
        super().__init__("div", **properties)


class Script(_SETag):
    def __init__(self, **properties):
        super().__init__("script", **properties)
    def __exit__(self, *args):
        super().__exit__(*args)
        _add("\n")

        
class Span(Tag):
    def __init__(self, **properties):
        super().__init__("span", **properties)


class I(Tag):
    def __init__(self, **properties):
        super().__init__("i", **properties)


class A(Tag):
    def __init__(self, **properties):
        super().__init__("i", **properties)


class B(Tag):
    def __init__(self, **properties):
        super().__init__("b", **properties)

        
def meta(**properties):
    tag("meta", **properties)
    _add("\n")


def link(**properties):
    tag("link", **properties)
    _add("\n")    

    
def text():
    global _text
    return _text
    


if __name__ == "__main__":
    print("Hello world")
    with Html(lang="en-US") as x:
        with Head():
            with Title():
                x += "Hello world"
        with Body():
            with H2():
                x += "Header"
            x += "content"
    print(text())
