import datetime
import calendar
import json
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.views import generic 
from django.views.generic import ListView, CreateView, TemplateView, FormView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
#, AddAccountForm # ユーザーアカウントフォーム #LoginForm
from .models import Report, Genre, Account, ControlMeasure, Comment, NGWord, KeyWord
from .forms import (ReportForm, CreatePost, AddGenre, SearchForm, CreativeControlMeasure, CreateComment, AddNgWord, AddKeyWord)#, AccountForm, UserCreationForm#, AddAccountForm # ユーザーアカウントフォーム #LoginForm
from .functions import (get_count, monthly_count, weekly_count, 
                        bymonth_count, get_count_chart, get_genre_chart, 
                        get_cm_chart, assign_cm)
                        
from django.contrib.auth.models import User

#データ抽出日付調整
d = datetime.date.today()
yd = (d - datetime.timedelta(days=1))
fd = d.replace(day=1)
ed = d.replace(day=calendar.monthrange(d.year, d.month)[1])

@login_required
def TopView(request):
    context = {}
    context["form_name"] = "main"
    return render(request, 'moticom/main.html', context)

#各ページ内容表示用
#ログイン画面
#class login(LoginView):
#    template_name = 'moticom/auth.html'

#ユーザ作成
def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #user.is_active = False
            user.save()
            messages.success(request, '登録完了！！！')
            return redirect('moticom:main')
    return render(request, 'moticom/auth.html', context)

#TOP
class IndexView(ListView):
    template_name = 'moticom/index.html'
    context_object_name = 'latest_report_list'
    
    #最新投稿10件の取得
    def get_queryset(self):
        return Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')[:10]
            
#現行使用版:グラフ用データを取得
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {}
        #日/週、日/月、月/年のグラフデータの取得
        context = get_count_chart(context, d, fd)
        
        return context


#掲示板
class BoardView(ListView):
    model = Report
    template_name = 'moticom/board.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['report_list'] = Report.objects.order_by('-created_at')
        context['genre_list'] = Genre.objects.all()
        return context
    
#ジャンル別表示処理
def genre_display(request):
    if request.method == 'GET':
        context = {
                   'report_list':Report.objects.filter(genre_id=request.GET.get('genre_id')).order_by('-created_at'),
                   'genre_list':Genre.objects.all(),
                   }
        return render(request, 'moticom/board.html', context)
    
#報告画面
class ReportView(FormView):
    template_name = 'moticom/report.html'
    form_class = ReportForm
    
    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST)
        if form.is_valid():
            request.session['request_text'] = request.POST.get('report_text')
            return redirect('moticom:genre')
        else:
            return render(request, 'moticom/report.html', {'form':form})

class GenreView(FormView):
    template_name = 'moticom/genre.html'
    model = Genre
    form_class = CreatePost
    
#ユーザーIDの取得と代入の必要あり
def create_post(request):
    if request.method == 'POST':
        if request.POST.get('anonymous'):
            form_contents = {
                'report_text':request.session['request_text'],
                'user_id':request.user.pk,
                'genre_id':request.POST.get('genre_id'),
                'cm_id':assign_cm(request.session['request_text']),
                'anonymous':True,
            }
        else:
            form_contents = {
                'report_text':request.session['request_text'],
                'user_id': request.user.pk,
                'genre_id':request.POST.get('genre_id'),
                'cm_id':assign_cm(request.session['request_text']),
                'anonymous':False,
            }
        form = CreatePost(form_contents)
        if form.is_valid():
            form.save()
            newPost = Report.objects.filter(user_id=request.user.pk).order_by('-created_at')[0]
        else:
            return redirect('moticom:genre')
            
    context = {
        'report_text':newPost.report_text,
        'genre_id':newPost.genre_id,
    }
        
    return render(request, 'moticom/complete.html', context)

#
class ProfileView(TemplateView):
    model = User
    template_name = 'moticom/profile.html'
    

#
class ComplaintsView(TemplateView):
    template_name = 'moticom/complaints.html'
    
#
class HelpView(TemplateView):
    template_name = 'moticom/help.html'
    
#管理者用（別アプリに分ける予定）
@login_required
def AdminView(request):
    return render(request, 'moticom/admin.html')
#class AdminView(TemplateView):
#    template_name = 'moticom/admin.html'
#
class AnalysisView(ListView):
    template_name = 'moticom/analysis.html'
    model = ControlMeasure
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {}
        context['genre_count'] = {}
        context['cm_count'] = {}
        #日/週、日/月、月/年のグラフデータの取得
        context = get_count_chart(context, d, fd)
        context = get_genre_chart(context)
        context = get_cm_chart(context)
        return context
        
        
#コメント投稿用
def Admin_BoardView(request):
    queryset = Report.objects.all().order_by('-created_at')
    if request.method == 'POST':
        comment_contents = {
            'comment_text':request.POST.get('comment_text'),
            'report_id':request.POST.get('report_id'),
        }
        comment = CreateComment(comment_contents)
        if comment.is_valid():
            comment.save()
            comment = CreateComment()
        else:
            return redirect('moticom:admin_board')
    
    else:
        comment = CreateComment()
    
    context = {
        'report_list': queryset,
        'genre_list':Genre.objects.all(),
        'form': comment
    }
    return render(request, 'moticom/admin_board.html', context)
#ジャンル別表示
def admin_genre_display(request):
    if request.method == 'GET':
        context = {
                   'report_list':Report.objects.filter(genre_id=request.GET.get('genre_id')).order_by('-created_at'),
                   'genre_list':Genre.objects.all(),
                   'form':CreateComment()
                   }
        return render(request, 'moticom/admin_board.html', context)

#投稿削除用
def DeletePost(request):
    if request.method == 'POST':
        Report.objects.get(id=request.POST.get('post_id')).delete()
    return redirect('moticom:admin_board')
    
#コメント削除用
def DeleteComment(request):
    if request.method == 'POST':
        Comment.objects.get(id=request.POST.get('comment_id')).delete()
    return redirect('moticom:admin_board')
#
#class UserView(generic.TemplateView):
#      template_name = 'moticom/user.html'

#def user(request):
#    user_list = Account.objects.all()
#    params = {'user_list':user_list}
#    return render(request, 'moticom/user.html', params)

class UserView(ListView):
    template_name = 'moticom/user.html'
    queryset = User.objects.filter(id__gt=1)
    context_object_name = 'user_list'

#
class LayoutView(TemplateView):
    template_name = 'moticom/layout.html'

#
class Genre_ManageView(CreateView):
    template_name = 'moticom/genre_manage.html'
    model = Genre
    form_class = AddGenre
    success_url = 'moticom/genre_manage.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['genre_list'] = Genre.objects.all()
        return context
        
def create_genre(request):
    if request.method == 'POST':
        add_genre_name = request.POST.get('genre_name')
        context = {
            'genre_list': Genre.objects.all(),
            'form': AddGenre(),
            'error': "同名のジャンルが既に存在します",
        }
        try:
            Genre.objects.get(genre_name = add_genre_name)
            return render(request, 'moticom/genre_manage.html', context)
        except:
            form_addgenre = {
                'genre_name': add_genre_name,
            }
        form = AddGenre(form_addgenre)
        if form.is_valid():
            form.save()

    return redirect('moticom:genre_manage')
    
def delete_genre(request):
    if request.method == 'POST':
        Genre.objects.get(id=request.POST.get('genre_id')).delete()
    return redirect('moticom:genre_manage')

#NGワード追加
class FilterView(FormView):
    template_name = 'moticom/filter.html'
    model = NGWord
    form_class = AddNgWord
    
    def post(self, request, *args, **kwargs):
        form = AddNgWord(request.POST)
        if form.is_valid():
            form.save()
        return redirect('moticom:filter')
        
    def get_context_data(self):
        context = super().get_context_data()
        context['ngword_list'] = NGWord.objects.all()
        return context
        
#NGワード削除
def delete_NGword(request):
    if request.method == 'POST':
        NGWord.objects.get(id=request.POST.get('ngword_id')).delete()
    return redirect('moticom:filter')

#
def sorting(request):
    report_list = Report.objects.all()
    params = {'report_list':report_list}
    return render(request, 'moticom/sorting.html', params)

#キーワード設定
class LinkingView(FormView):
    template_name = 'moticom/linking.html'
    model = KeyWord
    form_class = AddKeyWord
    
    def post(self, request, *args, **kwargs):
        form = AddKeyWord(request.POST)
        if form.is_valid():
            form.save()
        return redirect('moticom:linking')
    
    def get_context_data(self):
        context = super().get_context_data()
        context['keyword_list'] = KeyWord.objects.all()
        context['report_list'] = Report.objects.all()
        context['cm_list'] = ControlMeasure.objects.all()
        return context
        
def Switch_link(request):
    if request.method == 'POST':
        try:
            request.POST.get('cm_id')
        except NoValue:
            return redirect('moticom:linking')
        rep = Report.objects.get(id=request.POST.get('report_id'))
        rep.cm_id = ControlMeasure.objects.get(id=request.POST.get('cm_id'))
        rep.save()
    return redirect('moticom:linking')

def DeleteKeyWord(request):
    if request.method == 'POST':
        KeyWord.objects.get(id=request.POST.get('key_id')).delete()
    return redirect('moticom:linking')

#
class Cm_CreateView(ListView):
    template_name = 'moticom/cm_create.html'
    model         = ControlMeasure

class CreativeControlMeasureView(CreateView):
    template_name = "moticom/cm_create_forms.html"
    model         = ControlMeasure
    form_class    = CreativeControlMeasure
    success_url   =  "/moticom/cm_create" #正しいところに移ったときに修正
    def get_form(self):
        form = super(CreativeControlMeasureView, self).get_form()
        form.fields['cm_name'].label = '管理策名'
        form.fields['cm_contents'].label = '管理策'
        form.fields['genre_id'].label = 'ジャンル'
        return form
    
    
#管理策データ修正
class UpdateControlMeasureView(UpdateView):
    template_name = "moticom/cm_update_form.html"
    model         = ControlMeasure
    form_class    = CreativeControlMeasure
    success_url   = "/moticom/cm_create" #正しいところに移ったときに修正
    def get_form(self):
        form = super(UpdateControlMeasureView, self).get_form()
        form.fields['cm_name'].label = '管理策名'
        form.fields['cm_contents'].label = '管理策'
        form.fields['genre_id'].label = 'ジャンル'
        return form

#管理策データ削除
class DeleteControlMeasureView(DeleteView):
    template_name = "moticom/cm_delete_form.html"
    model = ControlMeasure
    success_url = "/moticom/cm_create" #正しいところに移ったときに修正

def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)
        
        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Report.objects.filter(Q(user_id__user_name__icontains = freeword)|Q(genre_id__genre_name__icontains = freeword)|Q(report_text__icontains = freeword))
            
        params = {
            'search_list':search_list,
        }
        
        return render(request, 'moticom/search.html', params)

#ユーザ登録機能
class SignUp(CreateView):
    template_name = 'moticom/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('moticom:signup_finish')
    
class SignUpFinish(TemplateView):
    template_name = 'moticom/signup_finish.html'
    

#class Login(LoginView):
#    form_class = LoginForm
#    template_name = 'moticom/login.html'
#    
#@login_required
#class Logout(LogoutView):
#    template_name = 'moticom/logout.html'

#class SignUp(CreateView):
#    form_class = SignUpForm
#    template_name = "moticom/signup.html" 
#    success_url = reverse_lazy('moticom:user')
#
#    def form_valid(self, form):
#        user = form.save() # formの情報を保存
#        login(self.request, user) # 認証
#        self.object = user 
#        return HttpResponseRedirect(self.get_success_url()) # リダイレクト
        
        
"""
#ログイン
#def Login(request):
#    # POST
#    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
#        ID = request.POST.get('username')
#        Pass = request.POST.get('password')

        # Djangoの認証機能
#        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
#        if user:
            #ユーザーアクティベート判定
#            if user.is_active:
                # ログイン
#                login(request,user)
                # ホームページ遷移
#                return HttpResponseRedirect(reverse('moticom:main'))
#            else:
                # アカウント利用不可
#                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
#        else:
#            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'moticom/login.html')
"""
#ログアウト
#@login_required
#def Logout(request):
#    logout(request)
#    # ログイン画面遷移
#    return HttpResponseRedirect(reverse('login'))


#class  SignUp(TemplateView):

#    def __init__(self):
#        self.params = {
#        "AccountCreate":False,
#        "account_form": AccountForm(),
        #"add_account_form":AddAccountForm(),
#        }

    # Get処理
#    def get(self,request):
#        self.params["account_form"] = AccountForm()
        #self.params["add_account_form"] = AddAccountForm()
#        self.params["AccountCreate"] = False
#        return render(request,"moticom/signup.html",context=self.params)

    # Post処理
#    def post(self,request):
#        self.params["account_form"] = AccountForm(data=request.POST)
        #self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # フォーム入力の有効検証
#        if self.params["account_form"].is_valid(): #and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
#            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            #account.set_password(account.password)
            # ハッシュ化パスワード更新
#            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            #add_account = self.params["add_account_form"].save(commit=False)
            #AccountForm & AddAccountForm 1vs1 紐付け
            #add_account.user = account

            # モデル保存
            #add_account.save()

            # アカウント作成情報更新
#            self.params["AccountCreate"] = True

#        else:
            # フォームが有効でない場合
#            print(self.params["account_form"].errors)

#        return render(request,"moticom/signup.html",context=self.params)
        

#class PasswordChange(LoginRequiredMixin, PasswordChangeView):
#    """パスワード変更ビュー"""
#    success_url = reverse_lazy('moticom:password_change_done')
#    template_name = 'moticom/password_change.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
#        context["form_name"] = "password_change"
#        return context

#class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
#    """パスワード変更完了"""
#    template_name = 'moticom/password_change_done.html'

#class PasswordChange(PasswordChangeView):
#    """パスワード変更ビュー"""
#    form_class = MyPasswordChangeForm
#    success_url = reverse_lazy('moticom:password_change_done')
#    template_name = 'moticom/password_change.html'


#class PasswordChangeDone(PasswordChangeDoneView):
#    """パスワード変更しました"""
#    template_name = 'moticom/password_change_done.html'
    

"""
変更点
・以下重複していた記述をコメントアウト
"""

"""
マージの際に記述が重複してしまったみたいです
重複していると思われるためコメントアウト

""
#ログイン画面
<<<<<<< HEAD
class Login(LoginView):
=======
import datetime
import calendar
import json
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, TemplateView, FormView, UpdateView, DeleteView
from django.db.models import Q

from .models import Report, Genre, Account, ControlMeasure, Comment, NGWord
from .forms import ReportForm, CreatePost, AddGenre, SearchForm, MyPasswordChangeForm, CreativeControlMeasure, CreateComment, AddNgWord, AccountForm, UserCreationForm#, AddAccountForm # ユーザーアカウントフォーム #LoginForm
from .functions import get_charts_count

#データ抽出日付調整
d = datetime.date.today()
yd = (d - datetime.timedelta(days=1))
fd = d.replace(day=1)
ed = d.replace(day=calendar.monthrange(d.year, d.month)[1])

#各ページ共通部品表示用（ヘッダー・フッター・サイドバー）
class TopView(TemplateView):#(LoginRequiredMixin,TemplateView):
    template_name = 'moticom/main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "main"
        return context

#各ページ内容表示用
""

"""
"""
#各ページ共通部品表示用（ヘッダー・フッター・サイドバー）
class TopView(LoginRequiredMixin,TemplateView):
    template_name = 'moticom/main.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "main"
        return context
"""
