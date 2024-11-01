from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
#django.views.genericからTemplateView、ListViewをインポート
from django.views.generic import TemplateView, ListView
#django.views.genericからTemplateViewをインポート
from django.views.generic import TemplateView
#django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
#django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
#formモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
#method_decoratorをインポート
from django.utils.decorators import method_decorator
#login_requiredをインポート
from django.contrib.auth.decorators import login_required
#modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost
#django.views.genericからDetailViewをインポート
from django.views.generic import DetailView
#django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView


class IndexView(ListView):
    '''トップページのビュー
    '''
    #index.htmlをレンダリングする
    template_name='index.html'
    #モデルBlogPostのオブジェクトにorder_by()を適用して
    #投稿日時の降順で並び替える
    queryset=PhotoPost.objects.order_by('-posted_at')
    #1ページに表示するレコードの件数
    paginate_by=9

#デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
#ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):

    #forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class=PhotoPostForm
    #レンダリングするテンプレート
    template_name="post_photo.html"
    #フォームデータ登録完了後のリダイレクト先
    success_url=reverse_lazy('photo:post_done')

    def form_valid(self, form):

        #commit=FalseにしてPOSTされたデータを取得
        postdata=form.save(commit=False)
        #投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user=self.request.user
        #投稿データをデータベースに登録
        postdata.save()

        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    
    Attributes:
        template_name:  レンダリングするテンプレート
    '''
    #index.htmlをレンダリングする
    template_name='post_success.html'

class CategoryView(ListView):
    '''カテゴリページのビュー
    
    Attributes:
        templates_name: レンダリングするテンプレート
        pagenate_by:    1ページに表示するレコードの件数
    '''
    #index.htmlをレンダリングする
    template_name='index.html'
    #1ページに表示するレコードの件数
    paginate_by=9

    def get_queryset(self):
        #self.kwargsでキーワードの辞書を取得し、
        #categoryキーの値(Categorysテーブルのid)を取得
        category_id=self.kwargs['category']
        #filter(フィールド名=id)で絞り込む
        categories=PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        
        #クエリによって取得されたレコードを返す
        return categories
    
class UserView(ListView):
    #index.htmlをレンダリングする
    template_name='index.html'
    #1ページに表示するレコードの件数
    paginate_by=9

    def get_queryset(self):
        #self.kwargsでキーワードの辞書を取得し、
        #userキーの値(ユーザーテーブルid)を取得
        user_id=self.kwargs['user']
        #filter(フィールド名=id)で絞り込む
        user_list=PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        
        #クエリによって取得されたレコードを返す
        return user_list
    
class DetailView(DetailView):
    '''詳細ページのビュー

    投稿記事の詳細を表示するのでDetailViewを継承する
    Attributes:
        template_name: レンダリングするテンプレート
        model:         モデルのクラス
    '''
    #post.htmlをレンダリングする
    template_name='detail.html'
    #クラス変数modelにモデルBlohPostを設定
    model=PhotoPost

class MypageView(ListView):
    #mypage.htmlをレンダリングする
    template_name='mypage.html'
    #1ページに表示するレコードの件数
    paginate_by=9

    def get_queryset(self):
        #現在ログインしているユーザー名はHttpRequest.userに格納されている
        #filter(userフィールド=userオブジェクト)で絞り込む
        queryset=PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        #クエリによって取得されたレコードを返す
        return queryset
    
class PhotoDeleteView(DeleteView):
    #操作の対象はPhptoPostモデル
    model=PhotoPost
    #photo_delete.htmlをレンダリングする
    template_name='photo_delete.html'
    #処理完了後にマイページにリダイレクト
    success_url=reverse_lazy('photo:mypage')

    def delete(self,request,*args,**kwargs):
        #スーパークラスのdelete()を実行
        return super().delete(request,*args,**kwargs)