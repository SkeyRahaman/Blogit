from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Profile, Subscribe, Tag, Post, Comments, WebsiteMeta
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            image=SimpleUploadedFile(
                name='test_image.jpg', 
                content=b'', 
                content_type='image/jpeg'
            )
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertTrue(self.profile.image)

    def test_slug_auto_generation(self):
        self.assertEqual(self.profile.slug, slugify(self.user.username))

    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), 'testuser')

    def test_one_to_one_relationship(self):
        self.assertEqual(self.profile.user, self.user)
        with self.assertRaises(Exception):
            # Try to create another profile for same user
            Profile.objects.create(user=self.user, bio='Another bio')


class SubscribeModelTest(TestCase):
    def setUp(self):
        self.subscribe = Subscribe.objects.create(
            email='test@example.com'
        )

    def test_subscribe_creation(self):
        self.assertEqual(self.subscribe.email, 'test@example.com')
        self.assertIsNotNone(self.subscribe.date)


class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(
            name='Django',
            description='Web framework'
        )

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Django')
        self.assertEqual(self.tag.description, 'Web framework')

    def test_slug_auto_generation(self):
        self.assertEqual(self.tag.slug, slugify(self.tag.name))

    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), 'Django')


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='author', 
            password='testpass123'
        )
        self.tag1 = Tag.objects.create(name='Python', description='Python language')
        self.tag2 = Tag.objects.create(name='Web', description='Web development')
        
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user,
            image=SimpleUploadedFile(
                name='test_post.jpg', 
                content=b'', 
                content_type='image/jpeg'
            )
        )
        self.post.tags.add(self.tag1, self.tag2)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post content')
        self.assertEqual(self.post.author.username, 'author')
        self.assertTrue(self.post.image)
        self.assertEqual(self.post.tags.count(), 2)

    def test_slug_auto_generation(self):
        self.assertEqual(self.post.slug, slugify(self.post.title))

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_view_count_default(self):
        self.assertIsNone(self.post.view_count)

    def test_is_featured_default(self):
        self.assertFalse(self.post.is_featured)

    def test_bookmarks_and_likes(self):
        # Test adding bookmarks and likes
        user1 = User.objects.create_user(username='user1', password='pass123')
        user2 = User.objects.create_user(username='user2', password='pass123')
        
        self.post.bookmarks.add(user1)
        self.post.likes.add(user1, user2)
        
        self.assertEqual(self.post.bookmarks.count(), 1)
        self.assertEqual(self.post.likes.count(), 2)


class CommentsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='commenter', 
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Post for Comments',
            content='Content',
            author=self.user
        )
        self.comment = Comments.objects.create(
            content='Test comment',
            name='Test User',
            email='user@example.com',
            website='https://example.com',
            post=self.post,
            author=self.user
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'Test comment')
        self.assertEqual(self.comment.name, 'Test User')
        self.assertEqual(self.comment.email, 'user@example.com')
        self.assertEqual(self.comment.website, 'https://example.com')
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertIsNotNone(self.comment.date)

    def test_reply_comment(self):
        reply = Comments.objects.create(
            content='Reply comment',
            name='Reply User',
            email='reply@example.com',
            post=self.post,
            parent=self.comment
        )
        self.assertEqual(reply.parent, self.comment)
        self.assertEqual(self.comment.replies.first(), reply)


class WebsiteMetaModelTest(TestCase):
    def setUp(self):
        self.meta = WebsiteMeta.objects.create(
            title='Test Blog',
            description='A test blog description',
            about='About the test blog',
            name='Test Name',
            email='test@example.com',
            linkedin='https://linkedin.com/test',
            github='https://github.com/test',
            portfolio='https://portfolio.test'
        )

    def test_website_meta_creation(self):
        self.assertEqual(self.meta.title, 'Test Blog')
        self.assertEqual(self.meta.description, 'A test blog description')
        self.assertEqual(self.meta.about, 'About the test blog')
        self.assertEqual(self.meta.name, 'Test Name')
        self.assertEqual(self.meta.email, 'test@example.com')
        self.assertEqual(self.meta.linkedin, 'https://linkedin.com/test')
        self.assertEqual(self.meta.github, 'https://github.com/test')
        self.assertEqual(self.meta.portfolio, 'https://portfolio.test')

    def test_default_values(self):
        # Test that default values are used when not specified
        meta_with_defaults = WebsiteMeta.objects.create(
            title='Another Blog',
            description='Another description',
            about='Another about'
        )
        self.assertEqual(meta_with_defaults.name, 'Md Shakib Mondal')
        self.assertEqual(meta_with_defaults.email, 'sakibmondal7@gmail.com')
        self.assertEqual(meta_with_defaults.linkedin, 'https://www.linkedin.com/in/shakib-mondal/')
        self.assertEqual(meta_with_defaults.github, 'https://github.com/SkeyRahaman')
        self.assertEqual(meta_with_defaults.portfolio, 'http://sakibmondal7.pythonanywhere.com/')