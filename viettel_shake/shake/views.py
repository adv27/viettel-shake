import json
from collections import Counter

from django.shortcuts import redirect, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView
from sentry_sdk import capture_exception

from .models import Shake, ViettelUser
from .serializers import ShakeSerializer


def view_404(request, exception=None):
    # make a redirect to homepage
    return redirect(reverse('shake:index'))


class IndexTemplate(TemplateView):
    template_name = 'shake/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # get recently gifts
            gifts = Shake.gifts.all()
            gifts = list(gifts)
            gift_names = list(map(lambda g: g.data['data']['name'], gifts))
            counter = Counter(gift_names).most_common()
            context.update({
                'gifts': gifts[:400],
                'gifts_counter': counter
            })
        except Exception as e:
            capture_exception(e)
        return context

    @method_decorator(cache_page(30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


index_template_view = IndexTemplate.as_view()


class ViettelUserDetail(DetailView):
    model = ViettelUser
    slug_field = 'phone'
    slug_url_kwarg = 'phone'
    context_object_name = 'viettel_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shakes = self.object.shakes.all()
        context['shakes'] = shakes
        context['shakes_json'] = json.dumps(ShakeSerializer(shakes, many=True).data)
        return context


viettel_user_detail_view = ViettelUserDetail.as_view()
