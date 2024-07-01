from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import coverage

cov = coverage.Coverage()
cov.start()

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






cov.stop()
cov.save()
