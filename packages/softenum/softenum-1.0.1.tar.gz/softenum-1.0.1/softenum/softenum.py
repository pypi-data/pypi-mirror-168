Softenum = None

class Softenummeta(type):

    def __new__(metacls, cls, bases, classdict, **kwargs):       
        
        # Finding base __new__
        __new__ = classdict.get('__new__')

        use_args = True
        
        if __new__ is None:
            for base in bases:
                __new__ = getattr(base, "__new__")
                if __new__:
                    break
        
        # Avoid infinite loops
        if Softenum is not None:
             if __new__ is Softenum.__new__:
                __new__ = None

        if __new__ is None:
            __new__ = object.__new__
            use_args = False

        # Creating forbidden names list
        forbidden = set(("__module__", "__qualname__",))
        for member in cls.__dir__():
            forbidden.add(member)

        target_bases = bases + (object,)
        for base in target_bases:
            for key in base.__dict__:
                forbidden.add(key)

        # Creating response
        enum_members = {key: classdict[key] for key in classdict}
        
        # Avoiding forbidden
        for key in forbidden:
            if key in enum_members:
                del enum_members[key]

        # Cleaning classdict
        for member in enum_members:
            del classdict[member]

        enum_class = super().__new__(metacls, cls, bases, classdict, **kwargs)
        
        keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return','try', 'while', 'with', 'yield', '_', 'case', 'match']

        for member in enum_members:

            # if not re.match(r"^[a-z][a-z0-9_]*", member):
            if not member.isidentifier():
                raise Exception(f"Invalid enumerated value {member}: not identifier")
            if member in keywords:
                raise Exception(f"Invalid enumerated value {member}: kwlist")
                
            value = enum_members[member]
            if not isinstance(value, tuple):
                args = (value, )
            else:
                args = value

            if use_args:
                enum_member = __new__(enum_class, *args)
            else:
                enum_member = __new__(enum_class)

            enum_member._name_ = member
            enum_member._value_ = args
            enum_member.__objclass__ = enum_class
            enum_member.__init__(*args)

            setattr(enum_class, member, enum_member)

        return enum_class

    def __repr__(cls):
        return "<softenum %r>" % cls.__name__


class Softenum(metaclass=Softenummeta):

    def __new__(cls, value):

        if type(value) is cls:
            return value
        elif isinstance(value, cls):
            return value
        else:
            return cls(value)

    def __repr__(self):
        return "<%s.%s: %r>" % (
                self.__class__.__name__, self._name_, self._value_)

    def __str__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)
