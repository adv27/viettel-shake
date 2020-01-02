import json

from django.shortcuts import redirect, reverse
from django.views.generic import DetailView, TemplateView

from .models import ViettelUser
from .serializers import ShakeSerializer


def view_404(request, exception=None):
    # make a redirect to homepage
    return redirect(reverse('shake:index'))


class IndexTemplate(TemplateView):
    template_name = 'shake/index.html'


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
