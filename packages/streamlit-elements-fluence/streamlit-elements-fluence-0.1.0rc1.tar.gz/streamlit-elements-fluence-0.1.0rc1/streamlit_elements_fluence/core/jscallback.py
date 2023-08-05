class JSCallback:
    def __init__(self, javascript):
        self._javascript = javascript

    def __repr__(self):
        return self._javascript
