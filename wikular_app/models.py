from django.db import models
from django.utils import timezone
import random

class DocManager(models.Manager):
  def generate_id(self):
    num_digits = 5
    dictionary = 'abcdefghijklmnopqrstuvwxyz0123456789'
    while True:
      new_string_id = ''.join([random.choice(dictionary) for i in range(num_digits)])
      if not Doc.objects.filter(string_id=new_string_id).exists(): break
    return new_string_id

class Doc(models.Model):
  objects = DocManager()
  def __unicode__(self):
    return self.text[:50]
  def save(self):
    if not self.string_id:
      self.string_id = Doc.objects.generate_id()
      self.create_date = timezone.now()
    self.text = self.text.replace('\r\n', '\n')
    self.title = self.text.split('\n')[0]
    self.edit_date = timezone.now()
    super(Doc, self).save()
  text        = models.TextField()
  title       = models.CharField(max_length=200,default='My Great Document')
  string_id   = models.CharField(max_length=10,null=True)
  create_date = models.DateTimeField()
  edit_date   = models.DateTimeField()



