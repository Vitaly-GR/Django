from django.shortcuts import render, get_object_or_404
from .models import Bb, Category, AdvUser
from .forms import BbForm, ChangeUserInfo
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


@login_required
def profile(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'board/profile.html', context)


def other_page(request, page):
    try:
        template = get_template('board/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    bbs = Bb.objects.all()
    categories = Category.objects.all()
    context = {'bbs': bbs, 'categories': categories}
    return render(request, 'board/index.html', context)


def by_category(request, category_id):
    bbs = Bb.objects.filter(category=category_id)
    categories = Category.objects.all()
    current_category = Category.objects.get(pk=category_id)
    context = {'bbs': bbs,
               'categories': categories,
               'current_category': current_category
               }
    return render(request, 'board/by_category.html', context)


class BbCreateView(CreateView):
    template_name = 'board/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class BbLoginView(LoginView):
    template_name = 'board/login.html'


class BbLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'board/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'board/change_user_info.html'
    form_class = ChangeUserInfo
    success_url = reverse_lazy('board:profile')
    success_message = 'Данные успешно изменены =)'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BbPasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'board/password_change.html'
    success_url = reverse_lazy('board: profile')
    success_message = 'Пароль пользователя изменен'
