class Filter:
    """ Basic filter. All subclasses should override the apply function """

    def apply(self, data):
        raise NotImplementedError("Whoops. Contact the owner of the repo.")
