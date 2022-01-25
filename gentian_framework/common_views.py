"""Модуль стандартных классов представлений"""
from gentian_framework.templator import render


class PageNotFound404:
    """Класс представления - страница не найдена"""

    def __call__(self, request):
        return '404 WHAT', '404 Page Not Found'


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def post_process(self, request):
        data = self.get_request_data(request)
        self.create_object(data)
        return self.render_template_with_context()

    def create_object(self, data):
        pass

    def get_process(self, request):
        return self.render_template_with_context()

    def update_request(self, request):
        return request

    def __call__(self, request):
        if request['method'] == 'POST':
            return self.post_process(request)
        else:
            return self.get_process(request)
