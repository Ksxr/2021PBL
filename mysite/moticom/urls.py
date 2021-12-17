from django.urls import path, include

from . import views

from django.contrib.auth import views as auth_views

app_name = 'moticom'
urlpatterns = [
    path('', views.TopView, name='main'),
    #path('', views.TopView.as_view(), name='main'),
    path('index', views.IndexView.as_view(), name='index'),
    path('board', views.BoardView.as_view(), name='board'),
    path('genre_display', views.genre_display, name='genre_display'),
    path('report', views.ReportView.as_view(), name='report'),
    path('genre', views.GenreView.as_view(), name='genre'),
    path('complete', views.create_post, name='complete'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('complaints', views.ComplaintsView.as_view(), name='complaints'),
    path('help', views.HelpView.as_view(), name='help'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change_form'),    # 追加
    #path('accounts/password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_finish.html'), name='password_change_done'), 
    
    #管理者用ページ↓
    path('admin', views.AdminView, name='admin'),
    path('analysis', views.AnalysisView.as_view(), name='analysis'),
    path('admin_board', views.Admin_BoardView, name='admin_board'),
    path('admin_genre_display', views.admin_genre_display, name='admin_genre_display'),
    path('delete_post', views.DeletePost, name='delete_post'),
    path('delete_comment', views.DeleteComment, name='delete_comment'),
    path('user', views.UserView.as_view(), name='user'),
    path('layout', views.LayoutView.as_view(), name='layout'),
    path('genre_manage', views.Genre_ManageView.as_view(), name='genre_manage'),
    path('add_genre', views.create_genre, name='add_genre'),
    path('delete_genre', views.delete_genre, name='delete_genre'),
    path('filter', views.FilterView.as_view(), name='filter'),
    path('delete_NGword', views.delete_NGword, name='delete_NGword'),
    path('sorting', views.sorting, name='sorting'),
    path('linking', views.LinkingView.as_view(), name='linking'),
    path('switch_link', views.Switch_link, name='switch_link'),
    path('DeleteKeyWord', views.DeleteKeyWord, name='DeleteKeyWord'),
    path('cm_create', views.Cm_CreateView.as_view(), name='cm_create'),
    path('create', views.CreativeControlMeasureView.as_view(), name='create'),#正しいところに移ったらcm_createに修正
    path('<int:pk>/update', views.UpdateControlMeasureView.as_view(), name='update'), #正しいところに移ったらcm_updateに修正
    path('<int:pk>/delete', views.DeleteControlMeasureView.as_view(), name='delete'), #正しいところに移ったらcm_deleteに修正
    path('sorting', views.sorting, name='sorting'),
    path('linking', views.LinkingView.as_view(), name='linking'),
    path('search', views.Search, name='search'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('signup/finish', views.SignUpFinish.as_view(), name='signup_finish'),
    ]

"""
変更点
・コメントアウトされているものを下に移動
"""

"""
    #path('save_report', views.save_report, name='save_report'),
    #path('sorting', views.SortingView.as_view(), name='sorting'),
    #path('login/', views.Login, name='login'),
    #path('logout', views.Logout.as_view(), name='logout'),
    #path('password_change', views.PasswordChange.as_view(), name='password_change'), #パスワード変更
    #path('password_change/done', views.PasswordChangeDone.as_view(), name='password_change_done'), #パスワード完了
    #path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    #path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    #path('change_password/', auth_views.PasswordChangeView.as_view(template_name='moticom/password_change.html', success_url = '/'),name='password_change'),
    #path('password_change_form', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change_form'),    # 追加
    #path('password_change_done', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'), # 追加
   
"""