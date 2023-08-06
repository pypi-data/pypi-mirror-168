def new_builtins():
    class main:
        class dict(dict):
            def __add__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(other_val) is type(new_dict[other_key]):
                            new_dict[other_key] += other_val
                        else: raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be added together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                    else: new_dict[other_key] = other_val
                return new_dict
            def __radd__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(other_val) is type(new_dict[other_key]):
                            new_dict[other_key] += other_val
                        else: raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be added together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                    else: new_dict[other_key] = other_val
                return new_dict
            def __sub__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(new_dict[other_key]) is type(other_val):
                            new_dict[other_key] -= other_val
                        else: raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be subtract together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                return new_dict
            def __rsub__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(new_dict[other_key]) is type(other_val):
                            new_dict[other_key] -= other_val
                        else: raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be subtract together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                return new_dict
            def __mul__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(new_dict[other_key]) is type(other_val):
                            new_dict[other_key] *= other_val
                        else:
                            raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be multiply by together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                return new_dict
            def __rmul__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(new_dict[other_key]) is type(other_val):
                            new_dict[other_key] *= other_val
                        else:
                            raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be multiply by together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                return new_dict
            def __truediv__(self, other: dict):
                new_dict = self.copy()
                for other_key, other_val in other.items():
                    if other_key in new_dict:
                        if type(new_dict[other_key]) is type(other_val):
                            new_dict[other_key] /= other_val
                        else:
                            raise KeyError("\"" + other_key + "\" already exists in the dictionary, and the types cannot be divide by  together: %s + %s" % (type(other_val).__name__, type(new_dict[other_key]).__name__))
                return new_dict

        class Builtins_refactoring:
            def __init__(self): self.builtin_list = []
            def Add(self, obj): self.builtin_list.append(obj)
            def refactor(self, mode: str):
                for builtin_object in self.builtin_list:
                    if builtin_object is main.dict:
                        if mode == "curse":
                            from forbiddenfruit import curse
                            curse(dict, "__add__", builtin_object.__add__)
                            curse(dict, "__radd__", builtin_object.__radd__)
                            curse(dict, "__sub__", builtin_object.__sub__)
                            curse(dict, "__rsub__", builtin_object.__rsub__)
                            curse(dict, "__mul__", builtin_object.__mul__)
                            curse(dict, "__rmul__", builtin_object.__rmul__)
                        if mode == "builtins":
                            import builtins
                            builtins.dict = builtin_object
    return main()

