from django.db import models
from users.models import MyUser
from urllib.parse import urlparse
import bs4

class Olimpiada(models.Model):
    title = models.CharField(max_length=1900)
    url = models.URLField(max_length=10000)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ol_solves')

    def get_custom_url(self):
        parsed_url = urlparse(self.url)
        return parsed_url.netloc
    
    def __str__(self) -> str:
        return self.title
    
class Problem(models.Model):
    title = models.CharField(max_length=1900)
    url = models.URLField(max_length=10000)

    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ol_solve_problems')
    olimpiada = models.ForeignKey(Olimpiada, on_delete=models.CASCADE, related_name='problems')
    yechim = models.TextField()

    def get_custom_body(self):
        return bs4.BeautifulSoup(self.yechim, 'html.parser').get_text()

    def get_custom_url(self):
        parsed_url = urlparse(self.url)
        return parsed_url.netloc

    def __str__(self) -> str:
        return self.title