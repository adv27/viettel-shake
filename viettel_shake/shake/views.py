import json

from django.views.generic import DetailView, TemplateView

from .models import ViettelUser
from .serializers import ShakeSerializer


class IndexTemplateView(TemplateView):
    template_name = 'shake/index.html'


index_template_view = IndexTemplateView.as_view()


class ViettelUserDetailView(DetailView):
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


viettel_user_detail_view = ViettelUserDetailView.as_view()
