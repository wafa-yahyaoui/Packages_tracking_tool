from django.views import View
from django.template.response import HttpResponse


class RobotsTextView(View):

    def get(self, request):
        context_nobot_hr = ("User-Agent: * \n"
                            "Disallow: / "
                            )
        return HttpResponse(context_nobot_hr, content_type='text/plain')
