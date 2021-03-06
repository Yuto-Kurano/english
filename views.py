from django.shortcuts import render
from django.http import HttpResponse
from .forms import SignUpForm, CreateForm, SignInForm, EditForm, Create_myselfForm, CountForm, TwitterForm
from .models import Words, Sentence
from django.shortcuts import redirect
import requests, collections, matplotlib.pyplot as plt, seaborn as sns, tweepy, itertools
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from .secret_api import secret1, secret2, secret3, secret4

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
            params['msg'] = '検索できませんでした'
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
        try:
            try:#日本語入力時
                url = 'https://ejje.weblio.jp/content/' + word
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")
                meaning = soup.find(class_ = "content-explanation je").text#情報の取得
                params['msg'] = meaning
            except:#英語入力時
                url = 'https://ejje.weblio.jp/content/' + word
                html = requests.get(url)
                soup = BeautifulSoup(html.content, "html.parser")
                meaning = soup.find(class_ = "content-explanation ej").text#情報の取得
                params['msg'] = meaning
        except AttributeError:#スペルミスなどの場合
            params['msg'] = "検策できませんでした"
    return render(request, 'english/search.html', params)

def count(request, pk):#単語の使用頻度チェック
    params = {
        'title' : '単語頻度チェック',
        'form' : CountForm(),
        'msg' : '',
        'image' : '',
    }
    word_list = []
    try:
        if (request.method == 'POST'):
            form = CountForm(request.POST)
            count = request.POST['sentence']
            count = count.lower()
            count = count.replace(".", "")
            sentence = count.replace(",", "")
            word_list.append(sentence.split())#スペースで分割
            change = itertools.chain.from_iterable(word_list)#一次元配列に変換
            words = list(change)#y軸に入れられるように統一
            second_word_list = []
            emit_words = [
                "a", "an", "the",
            ]
            for sort_word in words:
                if (sort_word in emit_words) == False:#emit_wordsに記載の単語を排除
                    second_word_list.append(sort_word)
            collect = collections.Counter(second_word_list)#単語の数の計測
            popular = collect.most_common(20)#使用頻度上位20個抽出
            sns.set(context = "talk")#横棒グラフ
            fig = plt.subplots(figsize = (8,8))
            sns.countplot(y = second_word_list, order = [i[0] for i in popular])#グラフ作成
            filename = 'english/static/english/png/count.png'#フォルダ指定
            plt.savefig(filename)
    except:
        params['msg'] = 'a,an,theのみ入力していませんか？'
    return render(request, 'english/count.html', params)

def twitter(request, pk):
    params = {
        'form' : TwitterForm(),
        'msg' : '@から始まるアカウント名を入力してください',
        'danger' : '画面が切り替わらない場合はリロードしてください',
        'a' : '',
    }
    comsumer_key = secret1
    comsumer_secret = secret2
    access_token = secret3
    access_token_secret = secret4
    auth = tweepy.OAuthHandler(comsumer_key, comsumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    if (request.method == 'POST'):
        screen_name = request.POST['screen_name']
        try:
            #指定したユーザーの最新ツイートを7個取得、tweet_modeは以降のfull...で必要
            tweets = api.user_timeline(screen_name = screen_name, count = 7, tweet_mode = "extended")
            word_list = []#単語の一時的な格納先
            for tweet in tweets:
                params['a'] = tweet.user.screen_name
                 #記号を削除する
                count = str(tweet.full_text.lower()).replace(",", "")#full...をしなければ100文字制限が発生する
                count = count.replace(".", "")
                count = count.replace("!", "")
                count = count.replace("?", "")
                word = count.split()#スペースで単語ごとに区切る
                word_list.append(word)#リストaに格納
            change = itertools.chain.from_iterable(word_list)#一次元配列に変換
            words = list(change)#y軸に入れられるように統一
            second_word_list = []#最終的なリスト先
            #以下、主語→動詞→前置詞→接続詞→冠詞→否定+省略語の順で汎用度の高い単語を記述
            emit_words = [
                        "i", "you", "we", "he", "she", "they", "it", "this", "that",\
                        "be","am", "is", "are", "was", "were", "does", "did", "do",\
                        "at", "on", "in", "for", "to", "into", "of", "out", "as", "from", "with",\
                        "and", "or",\
                        "a", "an", "the",\
                        "not", "ain't", "aren't", "isn't", "wasn't", "weren't",\
                        "don't", "doesn't", "didn't", "haven't", "hasn't", "hadn't",\
                        "i'm", "you're", "he's", "she's", "they're", "it's", "that's"
                        ]
            for sort_word in words:
                if (sort_word in emit_words) == False:#emit_wordsに記載の単語を排除
                    second_word_list.append(sort_word)
            collect = collections.Counter(second_word_list)#単語の数の計測
            popular = collect.most_common(20)#使用頻度上位20個抽出
            sns.set(context = "talk")#横棒グラフ
            fig = plt.subplots(figsize = (13,13))#長い単語でも視認できる大きさに
            sns.countplot(y = second_word_list, order = [i[0] for i in popular])#グラフ作成
            filename = 'english/static/english/png/count_twitter.png'#フォルダ指定
            plt.savefig(filename)#上書き
        except:
            params['msg'] = 'このアカウントは存在しないかご利用いただけません'
    return render(request, 'english/twitter.html', params)
