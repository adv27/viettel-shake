import json

from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView

from .models import Shake, ViettelUser
from .serializers import ShakeSerializer


def view_404(request, exception=None):
    # make a redirect to homepage
    return redirect(reverse('shake:index'))


class IndexTemplate(TemplateView):
    template_name = 'shake/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get recently gifts
        query = \
            Q(data__status__code='SG0020') \
            | Q(data__status__code='SG0021') \
            | Q(data__status__code='SG0023')
        gifts = Shake.objects.exclude(query)[:400]
        context['gifts'] = gifts
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
