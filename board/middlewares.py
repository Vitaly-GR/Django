from .models import SubRubric


def board_context_processor(request):
    context = {'rubrics': SubRubric.objects.all(), 'keyword': '', 'all': ''}
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    return context
