
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve, reverse, reverse_lazy
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
import json

from django.views.generic.edit import DeleteView
from content.forms import NewsMonitorUpdateForm, ProjectUpdateForm
from content.models import News, NewsSources, Prices, Project, Category

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'content/news_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        context['section'] = 'news'
        p = Paginator(News.objects.all().exclude(status='IGNORE').order_by('-published_at'), self.paginate_by)
        context['newsitems'] = p.page(context['page_obj'].number)
        return context 


class NewsListBlockView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'content/news_blocks.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(NewsListBlockView, self).get_context_data(**kwargs)
        context['section'] = 'news'
        p = Paginator(News.objects.filter(status='PUBLISHED').exclude(domain__startswith="@",status='IGNORE').order_by('-published_at'), self.paginate_by)
        context['newsitems'] = p.page(context['page_obj'].number)
        return context 


class NewsListBigBlockView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'content/news_big_blocks.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(NewsListBigBlockView, self).get_context_data(**kwargs)
        context['section'] = 'news'
        p = Paginator(News.objects.filter(status='PUBLISHED',type='news').exclude(status='IGNORE',domain__startswith="@").order_by('-published_at'), self.paginate_by)
        context['newsitems'] = p.page(context['page_obj'].number)
        return context


def NewsMonitorView(request):
    news = News.objects.filter(status='RECEIVED').order_by('published_at').last()
    if news:
        return redirect('content:news-monitor-update',pk=news.id)
    else:
        return render(request, 'content/news_monitor_wait.html')

class NewsMonitorApproveAll(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        News.objects.filter(status='RECEIVED').update(status='PUBLISHED', expert_level='BASIC', sentiment='NEUTRAL')
        return HttpResponseRedirect(reverse('content:news-monitor'))

class NewsMonitorUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'content/news_monitor.html'
    form_class = NewsMonitorUpdateForm
    success_url = '/content/news_monitor'

    def form_valid(self, form):
        print(form.cleaned_data)
        print(f"form is valid and sentiment is {form.cleaned_data['sentiment']}")
        form.save()
        return HttpResponseRedirect(reverse('content:news-monitor'))

    def form_invalid(self, form):
        print("Form invalid")
        print(form.errors)
        return HttpResponseRedirect(reverse('content:news-monitor'))

    def get_context_data(self, **kwargs):
        context = super(NewsMonitorUpdateView, self).get_context_data(**kwargs)
        news_item = News.objects.get(pk=self.kwargs['pk'])
        context['news'] = news_item
        context['form'] = NewsMonitorUpdateForm(instance=news_item)
        return context 

    
def NewsIgnoreView(request, newsid):
    if News.objects.filter(id=newsid).exists():
        news = News.objects.get(id=newsid)
        news.status='IGNORE'
        news.save()
    else:
        print(f"News ID does not exists.. {newsid}")
    return HttpResponseRedirect(reverse('content:news-monitor'))

class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 50
    context_object_name = 'projects'
    template_name = 'content/project_list.html'

    def get_queryset(self):
        return Project.objects.all().order_by('marketcap_rank')


class ProjectsUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'content/project_update.html'
    form_class = ProjectUpdateForm
    success_url = reverse_lazy('content:projects-list')

class ProjectsDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('content:projects-list')
    template_name = "content/project_confirm_delete.html"


class PriceView(LoginRequiredMixin, ListView):
    model = Prices
    paginate_by = 19
    template_name = 'content/price_view1.html'
    context_object_name = 'prices'

    def get_queryset(self):
        return Prices.objects.filter(project__marketcap_rank__lte=1000).exclude(project__marketcap_rank__isnull=True).order_by('project__marketcap_rank')

class StatusImagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'content/status_images.html')