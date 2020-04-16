from django.test import TestCase
from django.urls import reverse
from django.test import SimpleTestCase
from .models import Project


class ProjectsViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_projects_list(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)


class ProjectDetailTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(
            name='Test Project',
            technologies='{django,test}',
            description='This is a test project.'
        )

    def test_default_pic(self):
        self.assertEqual(self.project.picture, 'default.png')

    def test_project_slug(self):
        response = self.client.get(
            reverse('projects'), kwargs={'slug': self.project.slug}
        )
        self.assertEqual(response.status_code, 200)

    def test_serve_project_pic(self):
        response = self.client.get(
            reverse('projects'), kwargs={'slug': self.project.slug}
        )
        self.assertContains(response, 'default.png')


class SessionTestCase(TestCase):
    def test_setting_session_messages(self):
        session = self.client.session
        message = 'This is a message test'
        session['message'] = message
        session['level'] = 'info'
        self.assertEqual(session['message'], message)
        self.assertEqual(session['level'], 'info')


class ErrorHandlerTestCase(SimpleTestCase):
    def test_404_handler_render(self):
        response = self.client.get('/does_not_exist/')
        self.assertContains(
            response,
            'Portfolio'
        )
