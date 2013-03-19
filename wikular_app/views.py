import json
from django.http import HttpResponse
from django.shortcuts import render
from wikular_app.models import Doc

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
  return render(request, 'wikular/docview', context)

def cmd(request):
  # TODO verify csrf
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
    request.POST['content']
    # { status : '', result : { page_id : '', content : '' } }
  if request.POST['action'] == 'sync_page':
    request.POST['page_id']
    request.POST['old_content']
    request.POST['new_content']
    # { status : '', result : { mergetype '': , content : '' } }
  return HttpResponse(request.__str__())


