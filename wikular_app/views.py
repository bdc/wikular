import json
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from wikular_app.models import Doc, DocManager
import mergepy

def index(request, string_id=''):
  context = {}
  if string_id:
    context['string_id'] = string_id
    try:
      doc = Doc.objects.get(string_id=string_id)
      context['msg'] = 'Page loaded!'
      context['doc_exists'] = True
      context['doc'] = doc
    except:
      context['doc_exists'] = False
      context['msg'] = 'Page not found. Start typing to create a new page'
  context.update(csrf(request))
  return render(request, 'wikular/docview', context)

def cmd(request):

  if request.POST['action'] == 'get_page':
    rsp = { 'status' : 'OK', 'result' : {} }
    try:
      doc = Doc.objects.get(string_id=request.POST['page_id'])
      rsp['result']['valid'] = True
      rsp['result']['content'] = doc.text
    except:
      rsp['result']['valid'] = False
    return HttpResponse(json.dumps(rsp))

  if request.POST['action'] == 'new_page':
    rsp = { 'status' : 'OK', 'result' : {} }
    try:
      doc = Doc(text = request.POST['content'])
      doc.save()
      rsp['result']['page_id'] = doc.string_id
      rsp['result']['content'] = doc.text
    except:
      rsp['status'] = 'error'
      rsp['msg'] = 'Error saving new page.'
    return HttpResponse(json.dumps(rsp))

  if request.POST['action'] == 'sync_page':
    rsp = { 'status' : 'OK', 'result' : {} }
    try:
      doc = Doc.objects.get(string_id=request.POST['page_id'])
      if doc.text == request.POST['old_content']:
        if doc.text == request.POST['new_content']:
          rsp['result']['mergetype'] = ''
          rsp['result']['content'] = doc.text
        else:
          doc.text = request.POST['new_content']
          doc.save()
          rsp['result']['mergetype'] = 'ff'
          rsp['result']['content'] = doc.text
      else:
        merge = mergepy.diff3w(request.POST['old_content'], doc.text, request.POST['new_content'])
        doc.text = merge
        doc.save()
        rsp['result']['mergetype'] = '3w'
        rsp['result']['content'] = doc.text
    except:
      rsp['status'] = 'error'
      rsp['msg'] = 'Error syncing page.'
  return HttpResponse(json.dumps(rsp))


