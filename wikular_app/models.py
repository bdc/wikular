from django.db import models
from django.utils import timezone

class Doc(models.Model):
  def __unicode__(self):
    return self.text[:50]
  def set_text(text):
    self.text = text
    self.title = text.split('\n')[0]
    self.edit_date = timezone.now()
  text        = models.TextField()
  title       = models.CharField(max_length=200,default='My Great Document')
  string_id   = models.CharField(max_length=10,null=True)
  create_date = models.DateTimeField()
  edit_date   = models.DateTimeField()



