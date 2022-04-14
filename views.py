from django.views.generic.base import TemplateView

DEMO_TEMPLATE_TAGS = [
    {'tag': 'user.first_name', 'description': 'Logged in user\'s first name.'},
    {'tag': 'user.last_name', 'description': 'Logged in user\'s last name.'},
    {'tag': 'user.email', 'description': 'Logged in user\'s email.'},
]

class PlaceholderModalView(TemplateView):
    template_name = "wagtail_placeholder/admin/placeholders_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = DEMO_TEMPLATE_TAGS
        return context