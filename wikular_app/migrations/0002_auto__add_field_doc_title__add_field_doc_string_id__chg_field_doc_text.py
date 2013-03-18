# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Doc.title'
        db.add_column(u'wikular_app_doc', 'title',
                      self.gf('django.db.models.fields.CharField')(default='My Great Document', max_length=200),
                      keep_default=False)

        # Adding field 'Doc.string_id'
        db.add_column(u'wikular_app_doc', 'string_id',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True),
                      keep_default=False)


        # Changing field 'Doc.text'
        db.alter_column(u'wikular_app_doc', 'text', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Deleting field 'Doc.title'
        db.delete_column(u'wikular_app_doc', 'title')

        # Deleting field 'Doc.string_id'
        db.delete_column(u'wikular_app_doc', 'string_id')


        # Changing field 'Doc.text'
        db.alter_column(u'wikular_app_doc', 'text', self.gf('django.db.models.fields.CharField')(max_length=1000000))

    models = {
        u'wikular_app.doc': {
            'Meta': {'object_name': 'Doc'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {}),
            'edit_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'My Great Document'", 'max_length': '200'})
        }
    }

    complete_apps = ['wikular_app']