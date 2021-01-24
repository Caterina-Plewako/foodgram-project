from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/default.html'


class AboutTechView(TemplateView):
    template_name = 'about/default.html'
