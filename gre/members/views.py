import csv, io, random, openai, json, pickle,os,base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template import loader
from google.oauth2 import credentials
from googleapiclient.discovery import build
from requests_oauthlib import OAuth2Session
from .models import Word
from .forms import LoginForm,RegisterForm,WordForm,UpdateForm


# 註冊
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  #重新導向登入畫面
        else:
            print(form.errors)  # 顯示表單錯誤以便調試
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

# 登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile/')  # 重新導向會員專屬頁面
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def update(request):
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            request.user.refresh_from_db()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = UpdateForm(instance=request.user)
    return render(request, 'update.html', {'form': form})



# def remember_word(request):
#     form = WordFrom
#     if request.method == "POST":
#         word = request.POST.get("word")
#         user.objects.update_or_create(get_all_word)
#         return HttpResponse("輸入成功")
#     return render(request,'')
        

# 讀入html並輸出
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

# 禁用csrf保護，不然無法完成功能
@csrf_exempt
def upload_csv(request):
    # 以UTF-8編碼讀取文件，並跳過第一行
    if request.method == 'POST':
        csv_file = request.FILES['file']
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        # 分割元素並寫入資料庫，有相同word則更新，無則創建新資料
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            created =  Word.objects.update_or_create(
                word=column[0],
                part_of_speech=column[1],
                meaning=column[2],
                #依難度調整level的數字
                level = 6
            )
        return HttpResponse("CSV文件已成功上傳並保存到資料庫中！")
    else:
        return render(request,"upload_csv.html")
    

def delete_all_word(request):
    # 刪庫走人
    words=Word.objects.all()
    words.delete()
    return HttpResponse("刪除成功!")
    
def get_all_word(request,key):
    # 讀取單字
    try:
        words = Word.objects.filter(level=key)
        return render(request,"words.html",{"words" : words,"key":key})
    except Exception as e:
        print(e)
        

def quiz(request):
    words = Word.objects.all()
    # 隨機選擇一個單詞作為問題
    question_word = random.choice(words)
    # 隨機選擇三個單詞作為錯誤答案
    wrong_words = random.sample([word for word in words if word != question_word], 3)
    # 將所有答案混合並隨機排序
    all_words = [question_word] + wrong_words
    random.shuffle(all_words)
    # 將正確答案儲存到 session 中
    request.session['correct_answer'] = question_word.word

    return render(request, 'quiz.html', {
        'question': question_word.meaning,
        'choices': [(word.word, word == question_word) for word in all_words]
    })


@login_required
def quiz2(request):
    # 接chatgpt api
    openai.api_key = request.user.openai_key
    # 取得問題的單字
    question_words = Word.objects.all()
    options = random.sample(list(question_words), 4)
    prompt = f"請回傳給我一題英文單字選擇題，格式如下：\n" \
             f"英文題目\n" \
             f"A. {options[0].word}\n" \
             f"B. {options[1].word}\n" \
             f"C. {options[2].word}\n" \
             f"D. {options[3].word}\n" \
             f"正確單字的選項（例如：'A'）\n" \
             f"範例如下:\n" \
             f"What is the synonym of commendation?\nA. praise\nB. criterion\nC. cassette\nD. temptation\n'answer:A. praise'"

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        response_message = completion.choices[0].message['content'].split("\n")
        
        question = response_message[0]
        options_text = response_message[1:5]
        correct_answer = response_message[5].split(":")[1].strip().rstrip("'")


        # 因為前端因素，將選項處理為字典
        options_dict = {opt.split(". ")[0]: opt.split(". ")[1] for opt in options_text}
        # 將正確答案存儲到session中
        request.session['correct_answer'] = correct_answer

        return render(request, 'quiz2.html', {
            'question': question,
            'options': options_dict  
        })

    except Exception as e:
        return HttpResponse(str(e))

def submit_answer(request):
    if request.method == 'POST':
        # 從POST請求中獲取答案
        answer = request.POST.get('answer')
        # 從session中獲取正確答案
        correct_answer = request.session.get('correct_answer')
        # 檢查答案是否正確
        is_correct = (answer == correct_answer)
        # 將結果儲存到 session 中
        request.session['is_correct'] = is_correct
        # 重定向到結果頁面
        return redirect('result')
    # 如果不是 POST 請求，則重定向到測驗頁面
    return redirect('quiz')

def result(request):
    
    # 從 session 中獲取答案
    is_correct = request.session.get('is_correct')
    return render(request, 'result.html', {
        'is_correct': is_correct,
    })

def authorize(request):

    # 載入憑證
    with open('client_secret_72064818004-snam4j27oel7vh7avgbs733bo5ipv4se.apps.googleusercontent.com.json', 'r') as read_file:
        credential = json.load(read_file)
        
    client_id = credential['web']['client_id']
    client_secret = credential['web']['client_secret']
    authorization_base_url = credential['web']['auth_uri']
    token_url = credential['web']['token_uri']
    redirect_uri = 'http://localhost:8080/oauth2/callback/'
    scope = ['https://www.googleapis.com/auth/cloud-platform']

    # 登入驗證
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url,access_type="offline", prompt="select_account")
    
    # 儲存以作驗證
    request.session['oauth_state'] = state
    print(f"Generated state: {state}")
    print(f"Stored state in session: {request.session.get('oauth_state')}")

    # 導向授權URL
    return redirect(authorization_url)

def callback(request):

    state = request.session.get('oauth_state')

    # 檢查是否存在錯誤參數
    error = request.GET.get('error')
    if error:
        return JsonResponse({'error': error, 'description': request.GET.get('error_description', '')}, status=403)

    # 讀取登入憑證
    with open('client_secret_72064818004-snam4j27oel7vh7avgbs733bo5ipv4se.apps.googleusercontent.com.json', 'r') as read_file:
        credential = json.load(read_file)

    client_id = credential['web']['client_id']
    client_secret = credential['web']['client_secret']
    token_url = credential['web']['token_uri']
    redirect_uri = 'http://localhost:8080/oauth2/callback/'

    # 讀取session中的state
    state = request.session.get('oauth_state')

    
    google = OAuth2Session(client_id, redirect_uri=redirect_uri, state=state)

    # 獲取回傳的授權碼與state
    code = request.GET.get('code')
    returned_state = request.GET.get('state')

    # # 驗證state是否匹配
    # if state != returned_state:
    #     return JsonResponse({'error': 'Invalid state parameter'}, status=400)

    try:
        # 使用授權碼獲得token
        creds_info = google.fetch_token(token_url, client_secret=client_secret, code=code)
        creds = credentials.Credentials(creds_info['access_token'])

        request.session['access_token'] = creds_info['access_token']

        return redirect('input_word')
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def convert_text_to_speech(request, word):
    access_token = request.session.get('access_token')
    
    # 使用token建立服務請求
    creds = credentials.Credentials(token=access_token)
    service = build('texttospeech', 'v1', credentials=creds)

    # 建立請求
    synthesis_input = {'text': word}
    voice = {'languageCode': 'en-US', 'name': 'en-US-Wavenet-D'}
    audio_config = {'audioEncoding': 'MP3'}

    # 發送請求並取得回應
    response = service.text().synthesize(
        body={
            'input': synthesis_input,
            'voice': voice,
            'audioConfig': audio_config
        }
    ).execute()

    #base64轉二進位
    audio_content = base64.b64decode(response['audioContent'])
    audio_dir = 'static/audio/'
    audio_path = os.path.join(audio_dir, f'{word}.mp3')
    
    # 確認文件夾
    os.makedirs(audio_dir, exist_ok=True)
    
    with open(audio_path, 'wb') as out:
        out.write(audio_content)
    
    return True

def input_word(request):
    form = WordForm()
    audio_path = None

    if request.method == 'POST':
        word = request.POST.get('word')
        if convert_text_to_speech(request, word):
            audio_path = f'/static/audio/{word}.mp3'
        
    context = {
        'form': form,
        'audio_path': audio_path,
        'word': word if audio_path else None
    } 
    return render(request, 'input_word.html', context)
