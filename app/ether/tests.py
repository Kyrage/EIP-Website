
from django.contrib.auth import get_user_model, authenticate
from django.template.defaultfilters import slugify
from django.test import TestCase
from .models import *

class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Testeur', password='test', email='test@dev.fr')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='Testeur', password='test')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='test')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='Testeur', password='wrong')
        self.assertFalse((user is not None) and user.is_authenticated)

class ProfileTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Testeur', password='test', email='test@dev.fr')
        self.user.save()
        self.profile = Profile.objects.create()

    def tearDown(self):
        self.user.delete()
        self.profile.delete()

    def test_valid_profile(self):
        self.profile.location = 'Lille'
        self.profile.birthdate = '1999-03-29'
        self.profile.save()
        self.assertEqual('Lille', self.profile.location)
        self.assertEqual('1999-03-29', self.profile.birthdate)

class NewsletterTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Testeur', password='test', email='test@dev.fr')
        self.user.save()
        self.newsletter = Newsletter.objects.create()

    def tearDown(self):
        self.user.delete()
        self.newsletter.delete()

    def test_user_can_suscribe(self):
        self.newsletter.email = self.user.email
        self.newsletter.registered = True
        self.newsletter.save()
        get = Newsletter.objects.filter(email=self.user.email).values('registered')
        self.assertTrue(get[0]['registered'])

    def test_user_can_unsuscribe(self):
        pass

class GameTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Testeur', password='test', email='test@dev.fr')
        self.user.save()
        self.game = Game.objects.create()
        self.game.user = self.user

    def tearDown(self):
        self.user.delete()
        self.game.delete()

    def test_user_can_suscribe_alpha(self):
        self.game.alpha = True
        self.game.save()
        self.assertTrue(self.game.alpha)

    def test_user_can_suscribe_beta(self):
        self.game.beta = True
        self.game.save()
        self.assertTrue(self.game.beta)

    def test_user_can_unsuscribe_alpha(self):
        pass

    def test_user_can_unsuscribe_beta(self):
        pass

class PostTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Testeur', password='test', email='test@dev.fr')
        self.user.save()
        self.post = Post.objects.create()
        self.post.author = self.user

    def tearDown(self):
        self.user.delete()
        self.post.delete()

    def test_post_has_slug(self):
        self.post.title = 'My first post'
        self.post.description = "It's a new post"
        self.post.slug = slugify(self.post.title)
        self.post.save()
        self.assertEqual(self.post.slug, slugify(self.post.title))