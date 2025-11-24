class NagList(list):
    """Enhanced list class with convenience methods for Nagios objects.
    
    NagList extends Python's built-in list to provide convenient attribute-based
    access to Nagios objects. It allows accessing items by name and provides
    special properties for common operations.
    
    Properties:
        first: Returns the first item in the list, or None if empty
        names: Returns a list of names of all items in the list
    
    Attribute Access:
        Items can be accessed by their 'name' attribute using dot notation.
        If multiple items have the same name, an AttributeError is raised.
    
    Example:
        >>> hosts = nag.hosts  # hosts is a NagList
        >>> first_host = hosts.first
        >>> host_names = hosts.names
        >>> specific_host = hosts.webserver  # Access by name
    """
    def __getattr__(self, name):
        """Get item by name attribute or access special properties.
        
        Args:
            name (str): Either 'first', 'names', or the name of an item to find
        
        Returns:
            Various: Depends on the attribute:
                    - 'first': First item in list or None
                    - 'names': List of all item names
                    - item name: The matching item object
        
        Raises:
            AttributeError: If name not found or multiple items have same name
        """

        if name == 'first':
            if self:
                return self[0]
            else:
                return None

        if name == 'names':
            return [x.name for x in self]

        obj = [x for x in self if x.name == name]
        if obj:
            if len(obj) == 1:
                return obj[0]
            else:
                raise AttributeError('Multiple instances found')

        raise AttributeError
