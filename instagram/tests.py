from django.test import TestCase
from .models import Article,Profile

# Create your tests here.
class ProfileTestClass(TestCase):

    #set up method
    def setUp(self):
        self.james=Profile(first_name = 'James', last_name = 'Muriuki', email ='james@moringaschool.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.james,Profile))


class ArticleTestClass(TestCase):

    def setUp(self):
        self.james=Editor(first_name = 'James', last_name = 'Muriuki', email = 'james@moringaschool.com')
        self.james.save_editor()

        self.new_tag = tags(name = 'testing')
        self.new_tag.save()

        self.new_article= Article(title = 'Test Article', post = 'This is a random tgest Post', editor = self.james)
        self.new_article.save()
        self.new_article.tags.add(self.new_tag)

    def tearDowm(self):
        Editor.objects.all().delete()
        tags.objects.all().delete()
        Article.objects.all().delete()

    def test_get_news_today(self):
        today_news = Article.today_news()
        self.assertTrue(len(today_news)>0)

    def test_get_news_by_date(self):
        test_date = '2017-03-17'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date)==0)
