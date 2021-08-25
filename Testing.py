import os
import  unittest
#import agri
from agri import app
class testClass(unittest.TestCase):
    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF_CSRF_ENABLED'] = False
        #app.config['DEBUG'] = False
        self.app=app.test_client()
    def tearDown(self):
        pass
    def test_slash(self):
        print('Home Page test')
        resp=self.app.get('/',content_type='html/text')
        #self.assertTrue(b'Successfully Logged in'in resp.data)
        self.assertEqual(resp.status_code,200)
    def test_login(self):
        print('Login test')
        resp=self.app.post('/login',data=dict(username='Karthik',password='abcdefg'),follow_redirects=True)
        #resp=self.app.get('/portal',follow_redirects=True)
        self.assertIn(b'Welcome Karthik!!',resp.data)
    def test_signup(self):
        print('Register test')
        resp=self.app.post('/register',data=dict(name='Madhu',mobileno='9845939375',lang='Kannada',email='karthikks.cs17@rvce.edu.in',password='abcdefg',confirm='abcdefg'),follow_redirects=True)
        #resp=self.app.get('/',follow_redirects=True)        
        self.assertEqual(resp.status_code,200)
        self.assertIn(b'Login',resp.data)
    def test_forgotpass(self):
        print('Forgot Password Test')
        resp=self.app.post('/forgotpass',data=dict(email='karthikks.cs17@rvce.edu.in'),follow_redirects=True)
        self.assertEqual(resp.status_code,200)
        self.assertIn(b'Password sent to the registered Email Address!',resp.data)
    def test_doc(self):
        print('Upload document test')
        resp=self.app.post('/login',data=dict(username='Karthik',password='abcdefg'),follow_redirects=True)
        resp=self.app.post('/upload/17/Karthik/karthikks.cs17@rvce.edu.in/7204250170/Kananda',data=dict(size='4',file='download2.jpg'),follow_redirects=True)
        self.assertEqual(resp.status_code,400)
        self.assertIn(b'Options',resp.data)
    def test_feedback(self):
        resp=self.app.post('/login',data=dict(username='Karthik',password='abcdefg'),follow_redirects=True)
        resp=self.app.post('/feedback/17/Karthik/karthikks.cs17@rvce.edu.in/7204250170/Kananda',data=dict(fd='goodwebsite'),follow_redirects=True)
        #resp=self.app.get('/portal',follow_redirects=True)                
        self.assertEqual(resp.status_code,200)           
        self.assertIn(b'Submitted Successully!',resp.data)
if __name__=='__main__':
    unittest.main()