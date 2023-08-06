"""This is the base class for argument.

If you want create your own argument classe, you muss inherits this class.
"""

class Argument() :
    """Base class for argument."""

    def __init__(self, name, description="", optional=False, deprecated=False) :
        """Create an argument
        
        name is the name of the argument
        description is the description of the argument (for help)
        optional is False if we must give this argument
        depracated says if the argument is a deprecated one
        """
        self.set_name(name)
        self.set_description(description)
        self.set_optional(optional)
        self.set_deprecated(deprecated)

    def get_name(self) :
        """Return the name of the argument."""
        return self._name

    def set_name(self, name) :
        """Change arguments name"""
        self._name = name
    
    def get_description(self) :
        """Return the description of the argument."""
        return self._description

    def set_description(self, description) :
        """Change the description of the argument."""
        self._description = description

    def get_optional(self) :
        """Return if the argument is optional."""
        return self._optional

    def set_optional(self, optional) :
        """Make the argument optionnal or not."""
        self._optional = optional
    
    def get_deprecated(self) :
        """Return if the argument is deprecated."""
        return self._deprecated

    def set_deprecated(self, deprecated) :
        """Make the argument optionnal or not."""
        self._optional = deprecated

    name = property(get_name, set_name)
    description = property(get_description, set_description)
    optional = property(get_optional, set_optional)
    deprecated = property(get_deprecated, set_deprecated)