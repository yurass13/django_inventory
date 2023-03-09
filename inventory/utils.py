
class ViewModelContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        if 'title' not in context:
            context['title'] = self.model.__name__

        # # NOTE if Set is empty we show only table data_header
        context['data_header'] = [field.name for field in self.model._meta.fields]
        return context