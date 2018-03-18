from forms import ContentEmailForm
from constants import STATUS_VIEW
from models import StatusDelivery
from ..abstract.models import TemplateEmail


def SplitPostRequest(req):
    my_dict = dict(req.iterlists())
    out_dict = {}
    index = 0
    status_dict = {}
    for i in my_dict[u'status']:
        status_dict[index] = i
        out_dict[i] = {}
        index += 1
    for i in my_dict:
        index = 0
        for j in my_dict[i]:
            out_dict[status_dict[index]].update({i:j})
            index += 1
    print out_dict
    return out_dict


def GetContextStatus():
    ob = StatusDelivery.objects.all()
    context = {}
    for i in ob:
        context[i.code] = i.id
    return context


def update_context(instance, post_or_get=None):
    context = {}

    for i in instance:
        name = i.status_delivery.name
        if (post_or_get is not None):
            context[STATUS_VIEW[name]] = ContentEmailForm(post_or_get, instance=i)
        else:
            context[STATUS_VIEW[name]] = ContentEmailForm(instance=i)
    for keys in STATUS_VIEW:
        if not STATUS_VIEW[keys] in context:
            if (post_or_get is not None):
                context[STATUS_VIEW[keys]] = ContentEmailForm(post_or_get)
            else:
                context[STATUS_VIEW[keys]] = ContentEmailForm(initial={'template_email': TemplateEmail.objects.all()[0],
                                                                       })
                # 'status_delivery': StatusDelivery.objects.get()
                #     code=keys),
                # 'store':store
    return context
