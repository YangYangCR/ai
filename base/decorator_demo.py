
registry = {}

def register(name):
    def decorator(cls):
        registry[name] = cls
        return cls
    return decorator

@register("cat")
class Cat:
    pass


if __name__ == '__main__':
    print(registry.values())