def default_message(message_builder):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if kwargs.get("message") is None:
                kwargs["message"] = message_builder(*args)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class DataValidation:
    def validates(self, attribute_name, data, **kwargs):
        if kwargs.get("validation") == "presence":
            self.__presence_validation(data, attribute_name, message=kwargs.get("message"))
            
        if kwargs.get("validation") == "greather_than":
            self.__number_greather_than(data, kwargs.get("base_number"), attribute_name, message=kwargs.get("message"))
            
        if kwargs.get("validation") == "smaller_than":
            self.__number_smaller_than(data, kwargs.get("base_number"), attribute_name, message=kwargs.get("message"))
            
        if kwargs.get("validation") == "includes":
            self.__includes(data, kwargs.get("array"), attribute_name, message=kwargs.get("message"))
        
    
    @default_message(lambda data, name: f"{name} must be present")    
    def __presence_validation(self, data, name, message=None):
        if data is None or (not isinstance(data, (float)) and not data):
            self.errors.append(message)
    
    @default_message(lambda data, base_number, name: f"{name} must be greather than {base_number}")
    def __number_greather_than(self, data, base_number, name, message=None):
        if data is None:
            return
        if data <= base_number:
            self.errors.append(message)
            
    @default_message(lambda data, base_number, name: f"{name} must be smaller than {base_number}")
    def __number_smaller_than(self, data, base_number, name, message=None):
        if data is None :
            return
        if data >= base_number:
            self.errors.append(message)       
            
    @default_message(lambda data, array, name: f"{name} must be in {array}")
    def __includes(self, data, array, name, message=None):
        if data is None or array is None:
            return
        if data not in array:
            self.errors.append(message)  
        