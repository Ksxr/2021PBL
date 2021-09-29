import datetime
import calendar
import json
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Report

#データ抽出日付調整
d = datetime.date.today()
yd = (d - datetime.timedelta(days=1))
fd = yd.replace(day=1)
ed = yd.replace(day=calendar.monthrange(d.year, d.month)[1])

#各ページ共通部品表示用（ヘッダー・フッター・サイドバー）
class TopView(generic.TemplateView):
    template_name = 'moticom/main.html'

#各ページ内容表示用
#TOP
class IndexView(generic.ListView):
    template_name = 'moticom/index.html'
    context_object_name = 'latest_report_list'
    
    #最新投稿10件の取得
    def get_queryset(self):
        return Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')[:10]
    
    #グラフ用データを取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#        d_box = Report.objects.filter(created_at__date__range=[fd, ed])
        i = 1
        label_date =[fd + datetime.timedelta(days=i) for i in range(calendar.monthrange(d.year, d.month)[1])]
        data_list = []
        
        for i in label_date:
            data_list.append(Report.objects.filter(created_at__date=i).count())
        context['graph_date_list'] = json.dumps([i.strftime("%m/%d") for i in label_date])
        context['graph_data_list'] = json.dumps(data_list)
        return context
    
    
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['graph_data_list'] = Report.objects.filter(created_at__date = d)
#        return context

#掲示板
class BoardView(generic.ListView):
    queryset = Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')
    template_name = 'moticom/board.html'
    
#
class ReportView(generic.TemplateView):
    template_name = 'moticom/report.html'
    
#
class GenreView(generic.TemplateView):
    template_name = 'moticom/genre.html'

#
class CompleteView(generic.TemplateView):
    template_name = 'moticom/complete.html'
    
#
class ProfileView(generic.TemplateView):
    template_name = 'moticom/profile.html'

#
class ComplaintsView(generic.TemplateView):
    template_name = 'moticom/complaints.html'
    
#
class HelpView(generic.TemplateView):
    template_name = 'moticom/help.html'
    
#
class AdminView(generic.TemplateView):
    template_name = 'moticom/admin.html'

#
class AnalysisView(generic.TemplateView):
    template_name = 'moticom/analysis.html'

#
class UserView(generic.TemplateView):
    template_name = 'moticom/user.html'

#
class LayoutView(generic.TemplateView):
    template_name = 'moticom/layout.html'

#
class Genre_ManageView(generic.TemplateView):
    template_name = 'moticom/genre_manage.html'
    
#
class FilterView(generic.TemplateView):
    template_name = 'moticom/filter.html'
    
#
class SortingView(generic.TemplateView):
    template_name = 'moticom/sorting.html'

#
class LinkingView(generic.TemplateView):
    template_name = 'moticom/linking.html'