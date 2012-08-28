import re


REGISTRY = {}
hotlink_with_arg = re.compile(r"(\w+.\w+).(\d+):(\w+):(.*)")
hotlink_with_attr = re.compile(r"(\w+.\w+).(\d+):(\w+)")
hotlink_base = re.compile(r"(\w+.\w+).(\d+)")


class RegistrationError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def register(model, attr='get_absolute_url', prefix=''):
    if not hasattr(model, attr):
        raise RegistrationError('No such function for the model %s: %s' % (
            unicode(model), attr))


    model_name = "%s.%s" % (model._meta.app_label, model._meta.module_name)
    key = "%s.%s" % (model_name, attr)
    REGISTRY[key] = (model, attr, prefix)


def reverse_hotlink(hotlink):
    try:
        model_name, pk, attr, arg = hotlink_with_arg.match(hotlink).groups()
    except AttributeError:
        try:
            model_name, pk, attr = hotlink_with_attr.match(hotlink).groups()
            arg = None
        except AttributeError:
            try:
                model_name, pk = hotlink_base.match(hotlink).groups()
                attr = 'get_absolute_url'
                arg = None
            except AttributeError:
                return None

    key = "%s.%s" % (model_name, attr)
    try:
        model, attr, prefix = REGISTRY[key]
        try:
            instance = model.objects.get(pk=pk)
            func_or_prop = getattr(instance, attr)
            if arg:
                try:
                    return prefix + unicode(func_or_prop(int(arg)))
                except ValueError:
                    return prefix + unicode(func_or_prop(arg))
            else:
                if hasattr(func_or_prop, '__call__'):
                    return prefix + unicode(func_or_prop())
                else:
                    return prefix + unicode(func_or_prop)
        except model.DoesNotExist:
            return None
    except KeyError:
        return None


