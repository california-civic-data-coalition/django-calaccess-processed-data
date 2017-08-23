#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for tracking processing of CAL-ACCESS snapshots over time.
"""
from __future__ import unicode_literals
import os
from hurry.filesize import size as sizeformat
from django.apps import apps
from django.db import connection, models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_raw import get_data_directory
from calaccess_processed import archive_directory_path


@python_2_unicode_compatible
class ProcessedDataVersion(models.Model):
    """
    A version of CAL-ACCESS processed data.
    """
    raw_version = models.OneToOneField(
        'calaccess_raw.RawDataVersion',
        related_name='processed_version',
        verbose_name='raw data version',
        help_text='Foreign key referencing the raw data version processed'
    )
    process_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing started',
        help_text='Date and time when the processing of the CAL-ACCESS version'
                  ' started',
    )
    process_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time update finished',
        help_text='Date and time when the processing of the CAL-ACCESS version'
                  ' finished',
    )
    zip_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='cleaned files zip archive',
        help_text='An archive zip of processed files'
    )
    zip_size = models.BigIntegerField(
        null=True,
        verbose_name='zip of size (in bytes)',
        help_text='The expected size (in bytes) of the zip of processed files'
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        verbose_name = 'TRACKING: CAL-ACCESS processed data version'
        ordering = ('-process_start_datetime',)
        get_latest_by = 'process_start_datetime'

    def __str__(self):
        return str(self.raw_version.release_datetime)

    @property
    def update_completed(self):
        """
        Check if the database update to the version completed.

        Return True or False.
        """
        if self.process_finish_datetime:
            is_completed = True
        else:
            is_completed = False

        return is_completed

    @property
    def update_stalled(self):
        """
        Check if the database update to the version started but did not complete.

        Return True or False.
        """
        if self.process_start_datetime and not self.update_finish_datetime:
            is_stalled = True
        else:
            is_stalled = False

        return is_stalled

    def pretty_zip_size(self):
        """
        Returns a prettified version (e.g., "725M") of the zip's size.
        """
        if not self.zip_size:
            return None
        return sizeformat(self.zip_size)
    pretty_zip_size.short_description = 'processed zip size'
    pretty_zip_size.admin_order_field = 'processed zip size'


@python_2_unicode_compatible
class ProcessedDataFile(models.Model):
    """
    A data file included in a processed version of CAL-ACCESS.
    """
    version = models.ForeignKey(
        'ProcessedDataVersion',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='processed data version',
        help_text='Foreign key referencing the processed version of CAL-ACCESS'
    )
    file_name = models.CharField(
        max_length=100,
        verbose_name='processed data file name',
        help_text='Name of the processed data file without extension',
    )
    process_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing started',
        help_text='Date and time when the processing of the file started',
    )
    process_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing finished',
        help_text='Date and time when the processing of the file finished',
    )
    records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='records count',
        help_text='Count of records in the processed file'
    )
    file_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='archive of processed file',
        help_text='An archive of the processed file'
    )
    file_size = models.BigIntegerField(
        null=False,
        default=0,
        verbose_name='size of processed data file (in bytes)',
        help_text='Size of the processed file (in bytes)'
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        unique_together = (('version', 'file_name'),)
        verbose_name = 'TRACKING: processed CAL-ACCESS data file'
        ordering = ('-version_id', 'file_name',)

    def __str__(self):
        return self.file_name

    def copy_to_csv(self):
        """
        Copy the models objects to a csv_path.
        """
        if hasattr(self.model, 'copy_to_fields'):
            fields = self.model.copy_to_fields
            q = self.model.objects.values(*fields)
        elif hasattr(self.model, 'copy_to_expressions'):
            expressions = self.model.copy_to_expressions
            fields = expressions.keys()
        else:
            q = self.model.objects.all()

        copy_sql = "COPY (%s) TO STDOUT CSV HEADER;" % q.query

        with open(self.csv_path, 'wb') as stdout:
            with connection.cursor() as c:
                c.cursor.copy_expert(copy_sql, stdout)
        return

    def pretty_file_size(self):
        """
        Returns a prettified version (e.g., "725M") of the processed file's size.
        """
        return sizeformat(self.file_size)
    pretty_file_size.short_description = 'processed file size'
    pretty_file_size.admin_order_field = 'processed file size'

    def update_records_count(self):
        """
        Update records_count to the current number of records.
        """
        self.records_count = self.model.objects.count()
        self.save()

        return

    @property
    def csv_path(self):
        """
        Return the full path of where the ProcessedFile is locally stored.
        """
        return os.path.join(
            get_data_directory(), 'processed', '%s.csv' % self.file_name
        )

    @property
    def model(self):
        """
        Returns the ProcessedDataFile's corresponding database model object.
        """
        try:
            model = apps.get_model(
                'calaccess_processed',
                'OCD%sProxy' % self.file_name,
            )
        except LookupError:
            model_list = [
                m for m in apps.get_models()
                if m._meta.object_name == self.file_name
            ]
            try:
                model = model_list.pop()
            except IndexError:
                model = None

        return model
