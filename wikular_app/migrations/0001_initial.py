# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Doc'
        db.create_table(u'wikular_app_doc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1000000)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('edit_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'wikular_app', ['Doc'])


    def backwards(self, orm):
        # Deleting model 'Doc'
        db.delete_table(u'wikular_app_doc')


    models = {
        u'wikular_app.doc': {
            'Meta': {'object_name': 'Doc'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1000000'})
        }
    }

    complete_apps = ['wikular_app']