
class ViewModelContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if 'title' not in context:
            context['title'] = self.model.__name__

        return context