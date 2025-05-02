from django.test import TestCase
from django.contrib.auth.models import User
from app.forms import CommentForm, SubscribeForm, NewUserForm
from app.models import Post, Comments

class CommentFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )

    def test_comment_form_fields(self):
        form = CommentForm()
        self.assertEqual(set(form.fields), {'content', 'email', 'name', 'website'})

    def test_comment_form_placeholders(self):
        form = CommentForm()
        self.assertEqual(form.fields['content'].widget.attrs['placeholder'], 'Type your comment.....')
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Name')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email')
        self.assertEqual(form.fields['website'].widget.attrs['placeholder'], 'Website(optional)')

    def test_comment_form_valid_data(self):
        form_data = {
            'content': 'This is a test comment',
            'name': 'Test User',
            'email': 'test@example.com',
            'website': 'https://example.com'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_comment_form_missing_required_fields(self):
        form_data = {
            'content': '',  # required field
            'name': '',     # required field
            'email': '',    # required field
            'website': ''   # optional
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)  # website is optional


class SubscribeFormTest(TestCase):
    def test_subscribe_form_fields(self):
        form = SubscribeForm()
        self.assertEqual(list(form.fields), ['email'])

    def test_subscribe_form_placeholder(self):
        form = SubscribeForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Enter Your Email Here.')

    def test_subscribe_form_label(self):
        form = SubscribeForm()
        self.assertEqual(form.fields['email'].label, '')

    def test_subscribe_form_valid_data(self):
        form_data = {'email': 'test@example.com'}
        form = SubscribeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_subscribe_form_invalid_email(self):
        form_data = {'email': 'not-an-email'}
        form = SubscribeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_subscribe_form_empty_email(self):
        form_data = {'email': ''}
        form = SubscribeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class NewUserFormTest(TestCase):
    def test_new_user_form_fields(self):
        form = NewUserForm()
        self.assertEqual(set(form.fields), {'username', 'email', 'password1', 'password2'})

    def test_new_user_form_placeholders(self):
        form = NewUserForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'User name')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Create Password')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Confirm Password')

    def test_new_user_form_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = NewUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_new_user_form_duplicate_username(self):
        User.objects.create_user(username='existing', email='existing@example.com', password='testpass123')
        form_data = {
            'username': 'existing',  # duplicate
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0], 'User already exist.')

    def test_new_user_form_duplicate_email(self):
        User.objects.create_user(username='user1', email='existing@example.com', password='testpass123')
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # duplicate
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Email already exist.')

    def test_new_user_form_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'password123',
            'password2': 'differentpassword'  # mismatch
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'][0], 'Password Do not match.')

    def test_new_user_form_case_insensitive_username_check(self):
        User.objects.create_user(username='ExistingUser', email='existing@example.com', password='testpass123')
        form_data = {
            'username': 'existinguser',  # lowercase version of existing
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_new_user_form_case_insensitive_email_check(self):
        User.objects.create_user(username='user1', email='Existing@Example.com', password='testpass123')
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # lowercase version of existing
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = NewUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)