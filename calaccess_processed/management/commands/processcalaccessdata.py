#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data into processed CAL-ACCESS models, archive processed files and ZIP.
"""
import os
from django.conf import settings
from django.core.files import File
from django.utils.timezone import now
from django.core.management import call_command
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load data into processed CAL-ACCESS models, archive processed files and ZIP.
    """
    help = 'Load data into processed CAL-ACCESS models, archive processed files and ZIP.'

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        parser.add_argument(
            "--force-restart",
            "--restart",
            action="store_true",
            dest="restart",
            default=False,
            help="Force re-start (overrides auto-resume)."
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        # Set options
        super(Command, self).handle(*args, **options)
        self.force_restart = options.get("restart")

        # Get or create the logger record
        self.processed_version, created = self.get_or_create_processed_version()

        # If the version is already fully processed and we're not forcing a do-over
        # then just quit out now
        if self.processed_version.update_completed and not self.force_restart:
            msg_tmp = 'Processing completed at %s.'
            self.success(
                msg_tmp % self.processed_version.process_finish_datetime.ctime()
            )
            return False

        # Otherwise proceed with the standard routine
        # Firt, start the clock if created (or restart if forcing restart)
        if created or self.force_restart:
            self.processed_version.process_start_datetime = now()
            # also reset finish time if forcing re-start
            if self.force_restart:
                self.processed_version.process_finish_datetime = None
            self.processed_version.save()

        # then load
        self.load()

        # Zip only if django project setting enabled
        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            # then zip
            self.zip()

        # Wrap up the log
        self.processed_version.process_finish_datetime = now()
        self.processed_version.save()
        self.success('Processing complete')
        self.duration()

    def load(self):
        """
        Load all of the processed models.
        """
        call_command(
            'loadcalaccessfilings',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_restart=self.force_restart
        )
        self.duration()

        call_command(
            'loadocdelections',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

    def zip(self):
        """
        Zip up all processed data files and archive the zip.
        """
        if self.verbosity:
            self.header("Zipping processed files")

        # Remove previous zip file
        self.processed_version.zip_archive.delete()
        zip_path = os.path.join(self.data_dir, 'processed.zip')

        # enable zipfile compression
        compression = ZIP_DEFLATED

        try:
            zf = ZipFile(zip_path, 'w', compression, allowZip64=True)
        except RuntimeError:
            self.error('Zip file cannot be compressed (check zlib module).')
            compression = ZIP_STORED
            zf = ZipFile(zip_path, 'w', compression, allowZip64=True)

        # loop over and save files in csv processed data dir
        for f in os.listdir(self.processed_data_dir):
            if self.verbosity > 2:
                self.log(" Adding %s to zip" % f)
            csv_path = os.path.join(self.processed_data_dir, f)
            zf.write(csv_path, f)

        # close the zip file
        zf.close()
        if self.verbosity > 2:
            self.log(" All files zipped")

        # save the zip size
        self.processed_version.zip_size = os.path.getsize(zip_path)
        with open(zip_path, 'rb') as zf:
            # Save the zip on the processed data version
            if self.verbosity > 2:
                self.log(" Archiving zip")
            self.processed_version.zip_archive.save(
                os.path.basename(zip_path), File(zf)
            )
        if self.verbosity > 2:
            self.log(" Zip archived.")
