#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for more quickly loading bulk data.
"""
from __future__ import unicode_literals
import logging
from django.db import connection
from postgres_copy import CopyManager
logger = logging.getLogger(__name__)


class ConstraintsManager(CopyManager):
    """
    Utilities for more quickly loading bulk data.
    """
    def edit_schema(self, schema_editor, method_name, args):
        """
        Edits the schema without throwing errors.

        This allows for the add and drop methods to be run frequently and without fear.
        """
        try:
            getattr(schema_editor, method_name)(*args)
        except Exception:
            logger.debug("Edit unnecessary. Skipped")
            pass

    def add_constraints_and_indexes(self):
        """
        Re-create constraints and indexes on the model and its fields.
        """
        logger.debug("Adding constraints and indexes to {}".format(self.model.__name__))
        with connection.schema_editor() as schema_editor:
            # Add any "unique_together" contraints from the database
            if self.model._meta.unique_together:
                logger.debug("Adding unique_together of {}".format(self.model._meta.unique_together))
                args = (self.model, (), self.model._meta.unique_together)
                self.edit_schema(schema_editor, 'alter_unique_together', args)

            # Add any "index_together" contraints to the database.
            if self.model._meta.index_together:
                logger.debug("Adding index_together of {}".format(self.model._meta.index_together))
                args = (self.model, (), self.model._meta.index_together)
                self.edit_schema(schema_editor, 'alter_index_together', args)

            # Add any constraints to the fields
            for field in self.model.objects.constrained_fields:
                logger.debug("Adding constraints to {}".format(field))
                field_copy = field.__copy__()
                field_copy.db_constraint = False
                args = (self.model, field_copy, field)
                self.edit_schema(schema_editor, 'alter_field', args)

            # Add any indexes to the fields
            for field in self.model.objects.indexed_fields:
                logger.debug("Adding indexes to {}".format(field))
                field_copy = field.__copy__()
                field_copy.db_index = False
                args = (self.model, field_copy, field)
                self.edit_schema(schema_editor, 'alter_field', args)

    def drop_constraints_and_indexes(self):
        """
        Temporarily drop constraints and indexes on the model and its fields.
        """
        logger.debug("Dropping constraints and indexes from {}".format(self.model.__name__))
        with connection.schema_editor() as schema_editor:
            # Remove any "unique_together" constraints
            if self.model._meta.unique_together:
                logger.debug("Dropping unique_together of {}".format(self.model._meta.unique_together))
                args = (self.model, self.model._meta.unique_together, ())
                self.edit_schema(schema_editor, 'alter_unique_together', args)

            # Remove any "index_together" constraints
            logger.debug("Dropping index_together of {}".format(self.model._meta.index_together))
            if self.model._meta.index_together:
                args = (self.model, self.model._meta.index_together, ())
                self.edit_schema(schema_editor, 'alter_index_together', args)

            # Remove any field constraints
            for field in self.model.objects.constrained_fields:
                logger.debug("Dropping constraints from {}".format(field))
                field_copy = field.__copy__()
                field_copy.db_constraint = False
                args = (self.model, field, field_copy)
                self.edit_schema(schema_editor, 'alter_field', args)

            # Remove any field indexes
            for field in self.model.objects.indexed_fields:
                logger.debug("Dropping indexes from {}".format(field))
                field_copy = field.__copy__()
                field_copy.db_index = False
                args = (self.model, field, field_copy)
                self.edit_schema(schema_editor, 'alter_field', args)

    @property
    def constrained_fields(self):
        """
        Returns list of model's fields with db_constraint set to True.
        """
        return [
            f for f in self.model._meta.fields
            if hasattr(f, 'db_constraint') and f.db_constraint
        ]

    @property
    def indexed_fields(self):
        """
        Returns list of model's fields with db_index set to True.
        """
        return [
            f for f in self.model._meta.fields if f.db_index
        ]

    @property
    def db_table(self):
        """
        Return the model's database table name as a string.
        """
        return self._meta.db_table
