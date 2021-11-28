from django.shortcuts import render, get_object_or_404, redirect

from .models import Bb, Category, AdvUser
from .forms import BbForm, ChangeUserInfo, RegisterUserForm, SearchForm, AiFormSet
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .utilites import signer
from django.core.signing import BadSignature
from django.contrib.auth import logout
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


def author_detail(request, author_id):
    author = AdvUser.objects.get(pk=author_id)
    bb = Bb.objects.filter(author=author_id)

    return render(request, 'board/author_detail.html', {'author': author, 'bb': bb})


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'board/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'board/user_is_activated.html'
    else:
        template = 'board/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


@login_required
def profile(request):
    categories = Category.objects.all()
    bbs = Bb.objects.filter(author=request.user.pk)
    context = {'categories': categories, 'bbs': bbs}
    return render(request, 'board/profile.html', context)


def other_page(request, page):
    try:
        template = get_template('board/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    bbs = Bb.objects.all()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    paginator = Paginator(bbs, 5)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    form = SearchForm(initial={'keyword': keyword})
    categories = Category.objects.all()

    context = {'bbs': page.object_list, 'categories': categories, 'form': form, 'page': page}
    return render(request, 'board/index.html', context)


def by_category(request, category_slug):
    c = Category.objects.get(slug=category_slug)
    d = Category.objects.filter(super_category=c)
    if not d:
        bbs = Bb.objects.filter(category=c)
    else:
        bbs = Bb.objects.filter(category__super_category__slug=category_slug)

    categories = get_object_or_404(Category, slug=category_slug)

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 5)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'bbs': page.object_list,
               'categories': categories,
               'page': page,
               'form': form,

               }

    return render(request, 'board/by_category.html', context)


def detail(request, category_slug, slug):
    bb = Bb.objects.get(slug=slug)
    ais = bb.additionalimage_set.all()
    bbs = Bb.objects.all()
    bb.views += 1
    bb.save_base()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    context = {'bb': bb, 'ais': ais, 'form': form, 'bbs': bbs}
    return render(request, 'board/detail.html', context)


@login_required
def bb_create(request):
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AiFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
        return redirect('board:profile')
    else:
        form = BbForm(initial={'author': request.user.pk, 'contacts': f'{request.user.username}'})
        formset = AiFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'board/create.html', context)


@login_required
def bb_change(request, slug):
    bb = get_object_or_404(Bb, slug=slug)
    if request.method == 'POST':
        form = BbForm(request.POST, request.FILES, instance=bb)
        if form.is_valid():
            bb = form.save()
            formset = AiFormSet(request.POST, request.FILES, instance=bb)
        if formset.is_valid():
            formset.save()
            messages.add_message(request, messages.SUCCESS, 'Объявление исправлено')
        return redirect('board:profile')
    else:
        form = BbForm(instance=bb)
        formset = AiFormSet(instance=bb)
        context = {'form': form, 'formset': formset}
        return render(request, 'board/bb_change.html', context)


def bb_delete(request, slug):
    bb = get_object_or_404(Bb, slug=slug)
    if request.method == 'POST':
        bb.delete()
        messages.add_message(request, messages.SUCCESS, 'Объявление удалено')
        return redirect('board:profile')
    else:
        context = {'bb': bb}
        return render(request, 'board/bb_delete.html', context)


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


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'board/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('board:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'board/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'board/delete_user.html'
    success_url = reverse_lazy('board:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
