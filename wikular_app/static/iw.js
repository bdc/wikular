$(document).ready(function(){
  if(_get.page && _get.page !== '') {
    _iw.init_existing_page(_get.page, _get.text);
  }
  else {
    _iw.init_new_page();
  }
  if(_get.msg && _get.msg !== '') {
    _iw.notify_top(_get.msg);
  }
  else {
    _iw.notify_top('Start typing to create a new page.');
  }
  $('#content').keyup(_iw.content_change).focus();
  $(window).resize(function(){
    _iw.set_content_size();
  });
  _iw.set_content_size();
  _iw['polling_interval_id'] = setInterval(_iw.poll, 5000);
});

_iw = {}
_iw.init_existing_page = function(page_id, page_text) {
  _iw['page_id'] = page_id;
  $('#content').val(page_text);
  _iw['old_content'] = $('#content').val();
  _iw['sync_status'] = 'synced';
  window.history.replaceState(null, null, page_id);
}
_iw.init_new_page = function() {
  _iw['page_id'] = null;
  _iw['old_content'] = '';
  _iw['sync_status'] = 'synced';
  $('#content').val('');
  window.history.replaceState(null, null, '.');
}
_iw.poll = function() {
  if(_iw['sync_status'] === 'error') {
    _iw.content_change();
    return;
  }
  if(_iw['page_id'] && _iw['sync_status'] === 'synced' && _iw['old_content'] === $('#content').val()) {
    $.ajax({
      url: '_cmd',
      data: { action: 'get_page', page_id: _iw['page_id']},
      dataType: 'json',
      type: 'POST',
      headers: {'X-CSRFToken': $.cookie('csrftoken')},
    }).done(function(rsp) {
      if(rsp.status !== 'OK') {
        _iw['sync_status'] = 'error';
        console.log(rsp);
        return;
      }
      if( rsp.result.valid                           &&
          $('#content').val() === _iw['old_content'] &&
          rsp.result.content !== $('#content').val()  ) {
        $('#content').val(rsp.result.content);
        _iw['old_content'] = rsp.result.content;
        _iw.notify_top('Updating with remote edits.');
      }
      _iw['sync_status'] = 'synced';
    });
    _iw['sync_status'] = 'pending1';
  }
}
_iw.set_title = function() {
  $('title').html(/.*/.exec($('#content').val())[0]);
}
_iw.content_change = function(e) {
  window.clearTimeout(_iw['content_change_timeout']);
  _iw['content_change_timeout'] = setTimeout(_iw.try_save, 1000);
  _iw.set_title();
}
_iw.set_content_size = function() {
  $('#msg_holder').outerWidth(window.innerWidth);
  $('#sidebar_holder').css('top', $('#msg_holder').outerHeight());
  $('#sidebar_holder').outerHeight(window.innerHeight - $('#sidebar_holder').position().top);
  $('#content_holder').outerHeight(window.innerHeight - $('#content_holder').position().top);
  $('#content_holder').outerWidth (window.innerWidth  - $('#sidebar_holder').outerWidth());
}
_iw.try_save = function() {
  if(_iw['sync_status'] === 'synced' && _iw['old_content'] !== $('#content').val()) {
    _iw.save_page();
  }
  else if(_iw['sync_status'] === 'error') {
    _iw.save_page();
  }
}
_iw.load_page = function(page_id) {
  $.ajax({
    url: '_cmd',
    data: { action: 'get_page', page_id: page_id },
    dataType: 'json',
    type: 'POST',
    headers: {'X-CSRFToken': $.cookie('csrftoken')},
  }).done(function(rsp) {
    if(rsp.status !== 'OK') {
      _iw['sync_status'] = 'error';
      console.log(rsp);
      return;
    }
    if(!rsp.result.valid) {
      _iw.notify_top('Page not found. Start typing to create a new page.');
      _iw.init_new_page();
      return;
    }
    $('#content').val(rsp.result.content);
    _iw.notify_top('Page loaded.');
    _iw['old_content'] = rsp.result.content;
    _iw['sync_status'] = 'synced';
    _iw['page_id'] = page_id;
    _iw.set_title();
  });
  _iw['page_id'] = page_id;
  _iw['sync_status'] = 'loading';
  _iw.notify_top('Loading page...');
}
_iw.save_page = function() {
  if(!_iw['page_id']) {
    _iw.save_new_page();
    return;
  }
  $.ajax({
    url: '_cmd',
    data: { 
      action: 'sync_page', 
      page_id: _iw['page_id'], 
      old_content: _iw['old_content'],
      new_content: $('#content').val() },
    dataType: 'json',
    type: 'POST',
    headers: {'X-CSRFToken': $.cookie('csrftoken')},
  }).done(function(rsp) {
    if(rsp.status !== 'OK') {
      _iw['sync_status'] = 'error';
      console.log(rsp);
      return;
    }
    _iw['old_content'] = rsp.result.content;
    _iw['sync_status'] = 'synced';
    if(rsp.result.mergetype === '3w') {
      _iw.notify_top('Page saved with merge.');
      $('#content').val(rsp.result.content);
    }
    else
      _iw.notify_top('Page saved.');
  });
  _iw.notify_top('Saving...');
  _iw['sync_status'] = 'pending2';
}
_iw.save_new_page = function() {
  $.ajax({
    url: '_cmd',
    data: { action: 'new_page', content: $('#content').val() },
    dataType: 'json',
    type: 'POST',
    headers: {'X-CSRFToken': $.cookie('csrftoken')},
  }).done(function(rsp) {
    if(rsp.status !== 'OK') {
      _iw['sync_status'] = 'error';
      console.log(rsp);
      return;
    }
    _iw['page_id'] = rsp.result.page_id;
    _iw['old_content'] = rsp.result.content;
    _iw['sync_status'] = 'synced';
    window.history.replaceState(null, null, _iw['page_id']);
    _iw.notify_top('New page saved. Copy the URL above to access this page at any time.');
  });
  _iw.notify_top('Saving new page...');
  _iw['sync_status'] = 'pending3';
}
_iw.notify_top = function(str) {
  $('#msg').stop().fadeOut(200, function(){$('#msg').html(str).fadeIn(200);});
  window.clearTimeout(_iw['notify_top_timeout']);
  if(str !== '')
    _iw['notify_top_timeout'] = window.setTimeout(function(){_iw.notify_top('');}, 4000);
}




