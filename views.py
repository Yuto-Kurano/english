from django.shortcuts import render
from django.http import HttpResponse
from .forms import SignUpForm, CreateForm, SignInForm, EditForm, Create_myselfForm, CountForm
from .models import Words, Sentence
from django.shortcuts import redirect
import requests, collections, matplotlib.pyplot as plt, seaborn as sns, tweepy, itertools
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django_app.settings import secret1, secret2, secret3, secret4

def index(request):#紹介ページ
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

def signout(request, pk):
    if (request.method == 'POST'):
        logout(request)
        return redirect(to = 'index')
    params = {
        'title' : 'サインアウト',
        'msg' : 'サインアウトしますか？',
    }
    return render(request, 'english/signout.html', params)

def user_delete(request, pk):
    user = request.user
    data = Words.objects.filter(user = request.user)
    if (request.method == 'POST'):
        data.delete()
        user.delete()
        return redirect(to = 'index')
    params = {
        'title' : 'アカウント消去',
        'msg' : '本当に削除しますか？'
    }
    return render(request, 'english/user_delete.html', params)


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

def create_myself(request, pk):#単語と意味を手動で記録
    user = request.user
    params = {
        'title' : '単語追加',
        'form' : Create_myselfForm(),
        'goto' : 'mypage',
        'msg' : '単語を入力してください'
    }
    if(request.method == 'POST'):
        word = request.POST['word']
        meaning = request.POST['meaning']
        words = Words(word = word, meaning = meaning, user = user)
        words.save()
        return redirect(to = 'mypage', pk = user.pk)
    return render(request, 'english/create_myself.html', params)


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

def edit(request, num, pk):#単語編集
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

def search(request, pk):#単語検索
    params = {
        'title' : '検索',
        'form' : CreateForm(),
        'goto' : 'mypage',
        'msg' : '単語を入力してください',
        'meaning' : '',
        'origin' : '',
    }
    if(request.method == 'POST'):
        word = request.POST['word']
        try:#日本語入力時
            url = 'https://ejje.weblio.jp/content/' + word
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            meaning = soup.find(class_ = "content-explanation je").text
            params['msg'] = meaning
        except:#英語入力時
            url = 'https://ejje.weblio.jp/content/' + word
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser")
            meaning = soup.find(class_ = "content-explanation ej").text
            params['msg'] = meaning
    return render(request, 'english/search.html', params)

def count(request, pk):#単語の使用頻度チェック
    params = {
        'title' : '単語頻度チェック',
        'form' : CountForm(),
    }
    if (request.method == 'POST'):
        form = CountForm(request.POST)
        count = request.POST['sentence']
        count = count.lower()
        count = count.replace(".", "")
        sentence = count.replace(",", "")
        word = sentence.split()#スペースで分割
        collect = collections.Counter(word)#単語の数の計測
        popular = collect.most_common(20)#使用頻度上位20個抽出
        sns.set(context = "talk")#横棒グラフ
        fig = plt.subplots(figsize = (8,8))
        sns.countplot(y = word, order = [i[0] for i in popular])#グラフ作成
        filename = 'english/static/english/png/count.png'#フォルダ指定
        plt.savefig(filename)
    return render(request, 'english/count.html', params)

def twitter(request, pk):
    params = {
        'a' : '',
        'p' : '',
    }
    comsumer_key = secret1
    comsumer_secret = secret2
    access_token = secret3
    access_token_secret = secret4
    auth = tweepy.OAuthHandler(comsumer_key, comsumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    account = "dAp0IrD3VltQfP9"
    tweets = api.user_timeline(account = account, count = 100, tweet_mode = "extended")
    word_list = []#単語の格納先
    for tweet in tweets:
        count = str(tweet.full_text.lower()).replace(",", "")
        count = count.replace(".", "")
        word = count.split()
        word_list.append(word)#リストaに格納
    change = itertools.chain.from_iterable(word_list)#一次元配列に変換
    words = list(change)#y軸に入れられるように統一
    collect = collections.Counter(words)#単語の数の計測
    popular = collect.most_common(20)#使用頻度上位20個抽出
    sns.set(context = "talk")#横棒グラフ
    fig = plt.subplots(figsize = (8,8))
    sns.countplot(y = words, order = [i[0] for i in popular])#グラフ作成
    filename = 'english/static/english/png/count_twitter.png'#フォルダ指定
    plt.savefig(filename)    
    return render(request, 'english/twitter.html', params)