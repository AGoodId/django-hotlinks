import re
import django
from collections import namedtuple, defaultdict


REGISTRY = {}
hotlink_with_arg = re.compile(r"(\w+\.\w+)\.(\d+):(\w+):(.*)")
hotlink_with_attr = re.compile(r"(\w+\.\w+)\.(\d+):(\w+)")
hotlink_base = re.compile(r"(\w+\.\w+)\.(\d+)")

Hotlink = namedtuple('Hotlink', 'model_name pk attr arg')

class RegistrationError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def register(model, attr='get_absolute_url', prefix=''):
    if not hasattr(model, attr):
        raise RegistrationError('No such function for the model %s: %s' % (
            unicode(model), attr))

    if django.VERSION < (1, 7):
      model_name = "%s.%s" % (model._meta.app_label, model._meta.module_name)
    else:
      model_name = "%s.%s" % (model._meta.app_label, model._meta.model_name)
    key = "%s.%s" % (model_name, attr)
    REGISTRY[key] = (model, attr, prefix)


def parse_hotlink(hotlink):
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

    return Hotlink(model_name, pk, attr, arg)


def reverse_hotlinks(hotlinks):
    hotlinks = [parse_hotlink(h) for h in hotlinks]

    # Collect all instance pks of the same type
    keys = defaultdict(list)
    for h in hotlinks:
        if h is not None:
            key = "%s.%s" % (h.model_name, h.attr)
            keys[key].append(h.pk)

    # Batch database queries by type
    instances = defaultdict(dict)
    for key, pks in keys.items():
        model, attr, prefix = REGISTRY[key]
        qs = model.objects.filter(pk__in=pks)
        for obj in qs:
          instances[key][obj.pk] = obj

    # Get the reversed links
    results = []
    for hotlink in hotlinks:
        key = "%s.%s" % (hotlink.model_name, hotlink.attr)
        try:
            model, attr, prefix = REGISTRY[key]
            try:
                instance = instances[key][int(hotlink.pk)]
                func_or_prop = getattr(instance, attr)
                if hotlink.arg:
                    try:
                        result = prefix + unicode(func_or_prop(int(hotlink.arg)))
                    except ValueError:
                        result = prefix + unicode(func_or_prop(hotlink.arg))
                else:
                    if hasattr(func_or_prop, '__call__'):
                        result = prefix + unicode(func_or_prop())
                    else:
                        result = prefix + unicode(func_or_prop)
            except KeyError:
                result = None
        except:
            result = None
        results.append(result)
    return results


