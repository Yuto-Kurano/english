from django.shortcuts import render
from django.http import HttpResponse
from .forms import SignUpForm, CreateForm, SignInForm, EditForm
from .models import Words
from django.shortcuts import redirect
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login

def index(request):
    params = {
        'title' : '英単語アプリへようこそ!',
        'goto' : 'new',
        'goto' : 'login',
    }
    return render(request, 'english/index.html', params)

def signup(request):#新規登録
    if (request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to = 'mypage', pk = user.pk)
    else:
        form = SignUpForm()
    params = {
        'title' : '新規登録',
        'form' : form,
    }
    return render(request, 'english/signup.html', params)

def signin(request):#サインイン処理
    params = {
        'title' : 'ログイン画面',
        'form' : SignInForm(),
        'msg' : '入力してください',
    }
    if (request.method == 'POST'):
        form = SignInForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(to = 'mypage', pk = user.pk)
            else:
                params['msg'] = '有効なアカウントではありません'
                form = SignInForm()
        else:
            params['msg'] = 'usernameかpasswordが間違っています'
            form = SignInForm()
    return render(request, 'english/signin.html', params)

def mypage(request, pk):#個人ページ
    data = Words.objects.filter(user = request.user)#ログインユーザーのデータを抽出
    params = {
        'title' : 'マイページ',
        'data' : data,
        'goto' : 'create',
    }
    return render(request, 'english/mypage.html', params)

def create(request, pk):#単語追加
    user = request.user
    params = {
        'title' : '単語追加',
        'form' : CreateForm(),
        'goto' : 'mypage',
        'msg' : '単語を入力してください'
    }
    if(request.method == 'POST'):
        word = request.POST['word']
        try:
            # weblioのurlを取得(スクレイピング)
            url = 'https://ejje.weblio.jp/content/' + word
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            meaning = soup.find(class_ = "content-explanation ej").text
            words = Words(word = word, meaning = meaning, user = user)
            words.save()
            return redirect(to = 'mypage', pk = user.pk)
        except:#例外処理(英単語が存在しなかった場合)
            params['msg'] = 'It does not exist'
    return render(request, 'english/create.html', params)

def delete(request, num, pk):#単語削除
    user = request.user
    words = Words.objects.get(id = num)
    if(request.method == 'POST'):
        words.delete()
        return redirect(to = 'mypage', pk = user.pk)
    params = {
        'title' : '単語削除',
        'obj' : words,
        'id' : num,
        'goto' : 'mypage',
    }
    return render(request, 'english/delete.html', params)

def edit(request, num, pk):
    user = request.user
    obj = Words.objects.get(id = num)
    if(request.method == 'POST'):
        words = EditForm(request.POST, instance = obj)
        words.save()
        return redirect(to = 'mypage', pk = user.pk)
    params = {
        'title' : '編集',
        'id' :  num,
        'goto' : 'mypage',
        'form' : EditForm(instance = obj),
        'obj' : obj,
    }
    return render(request, 'english/edit.html', params)