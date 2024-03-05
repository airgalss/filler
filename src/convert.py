# decorator
def target(target_name):
    def decorator(func):
        Convert.instance().register(target_name, func)
        def wrapper(name, value):
           fn = Convert.instance().get(name)
           res = fn(value)
           return default_convert(res, name, value)
        return wrapper
    return decorator

class Convert:
    __instance = None
    def __init__(self):
        if self.__instance is None:
            self.function_map = dict()
            Convert.__instance = self
        else:
            raise Exception("cannot instantiate Namespace again.")
      
    @staticmethod
    def instance():
        if Convert.__instance is None:
            Convert()
        return Convert.__instance
    
    def register(self, name ,func):
        self.function_map[name] = func;

    def get(self, name):
        return self.function_map[name]

# Key Correction: just edit default_rule, you need not invoke it!
def default_convert(proposal_info, name, info):
    default_rule = {
        # ...
    }
    info.update(default_rule)
    return info