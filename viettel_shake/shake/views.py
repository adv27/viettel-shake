import json

from django.shortcuts import render
from django.views.generic import DetailView

from .models import ViettelUser
from .serializers import LoginSerializer, RequestLoginSerializer, ShakeSerializer


def index(request):
    context = {
        'request_login_serializer': RequestLoginSerializer,
        'login_serializer': LoginSerializer,
    }
    return render(request, 'shake/index.html', context)


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
