from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Word

#註冊測試
class TestSignUp(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_up_url = reverse('register') 

    def test_sign_up_GET(self):
        response = self.client.get(self.sign_up_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_sign_up_POST_form_valid(self):

        response = self.client.post(self.sign_up_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })

        self.assertEqual(response.status_code, 302)

    def test_sign_up_POST_form_invalid(self):
        response = self.client.post(self.sign_up_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'wrongpassword123',
        })

        self.assertEqual(response.status_code, 200)

#登入測試
class TestSignIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.sign_in_url = reverse('login')
        
        # 創建測試用戶
        CustomUser = get_user_model()
        self.test_user = CustomUser.objects.create_user(username='testuser', password='testpassword123')


    def test_sign_in_GET(self):
        response = self.client.get(self.sign_in_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_sign_in_POST_form_valid(self):
        response = self.client.post(self.sign_in_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })

        self.assertEqual(response.status_code, 302)  # 檢查是否重定向到會員專屬頁面

    def test_sign_in_POST_form_invalid(self):
        response = self.client.post(self.sign_in_url, {
            'username': 'wronguser',
            'password': 'wrongpassword123',
        })

        self.assertEqual(response.status_code, 200)  # 檢查是否仍停留在登入頁面
#更新會員資料測試
class TestUpdate(TestCase):
    def setUp(self):
        self.client = Client()
        self.update_url = reverse('update')

        # 創建測試用戶
        CustomUser = get_user_model()
        self.test_user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
  

    def test_update_url_in_GET_from_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"update.html")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code,302)

    
    def test_sign_in_POST_form_valid(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(self.update_url, {
            'word': 'testword',
            'openai_key': 'testopenai_key',
        })

        self.assertEqual(response.status_code, 302) 

#會員頁面測試
class TestpProfile(TestCase):
    def setUp(self):
        self.client = Client()
        self.update_url = reverse('profile')

        # 創建測試用戶
        CustomUser = get_user_model()
        self.test_user = CustomUser.objects.create_user(username='testuser', password='testpassword123')
  

    def test_update_url_in_GET_from_user(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"profile.html")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code,302)

#首頁測試
class TestpHome(TestCase):
    def setUp(self):
        self.client = Client()
        self.home = reverse("home")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.home)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"home.html")


#上傳csv測試
class TestpUploadCsv(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload = reverse("upload")

    def test_update_url_in_GET_from_visitor(self):
        response = self.client.get(self.upload)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"upload_csv.html")
    
    def test_upload_csv(self):
        # 創建一個 CSV 文件
        csv_content = "word,part_of_speech,meaning\nword1,noun,meaning1"
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode('utf-8'), content_type="text/csv")

        response = self.client.post(self.upload, {'file': csv_file})

        self.assertEqual(response.status_code, 200)

        # 檢查數據是否已保存到數據庫
        word = Word.objects.get(word='word1')
        self.assertEqual(word.part_of_speech, 'noun')
        self.assertEqual(word.meaning, 'meaning1')

        self.assertEqual(response.content.decode(), "CSV文件已成功上傳並保存到資料庫中！")

#單字頁面測試
class GetAllWordTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_all_word', args=[6])

        # 創建一些單詞
        Word.objects.create(word='word1', part_of_speech='noun', meaning='meaning1', level=6)
        Word.objects.create(word='word2', part_of_speech='verb', meaning='meaning2', level=6)

    def test_get_all_word(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "words.html")

        words = response.context['words']
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0].word, 'word1')
        self.assertEqual(words[1].word, 'word2')

#考試測試
class QuizTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.quiz_url = reverse('quiz')  
        self.submit_answer_url = reverse('submit_answer')  
        self.result_url = reverse('result')

        # 創建一些單詞
        Word.objects.create(word='word1', part_of_speech='noun', meaning='meaning1', level=6)
        Word.objects.create(word='word2', part_of_speech='verb', meaning='meaning2', level=6)
        Word.objects.create(word='word3', part_of_speech='verb', meaning='meaning3', level=6)
        Word.objects.create(word='word4', part_of_speech='noun', meaning='meaning4', level=6)

    def test_quiz(self):
        response = self.client.get(self.quiz_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "quiz.html")

        choices = response.context['choices']
        self.assertEqual(len(choices), 4)

    def test_submit_answer(self):
        # 提交答案
        response = self.client.post(self.submit_answer_url, {'answer': 'word1'})

        self.assertRedirects(response, self.result_url)

    def test_result(self):
        # 從 session 中設置答案
        session = self.client.session
        session['is_correct'] = True
        session.save()

        response = self.client.get(self.result_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "result.html")

        is_correct = response.context['is_correct']
        self.assertTrue(is_correct)



