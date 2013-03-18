from django.http import HttpResponse
from django.shortcuts import render
from wikular_app.models import Doc

def index(request, string_id=''):
  context = {}
  if string_id:
    context['string_id'] = string_id
    try:
      doc = Doc.objects.get(string_id=string_id)
      context['doc_exists'] = True
      context['doc'] = doc
    except:
      context['doc_exists'] = False
  return render(request, 'wikular/docview', context)


