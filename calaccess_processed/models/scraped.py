#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class BaseScrapedModel(models.Model):
    """
    Abstract base model from which all scraped models inherit.
    """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model options.
        """
        abstract = True


class BaseScrapedElection(BaseScrapedModel):
    """
    An election day scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for elections
    scraped as part of the candidates scraper, and one for elections scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        max_length=200
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class CandidateScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesscandidates` command.
    """
    scraped_id = models.CharField(
        verbose_name="election identification number",
        max_length=3,
        blank=True,
    )
    sort_index = models.IntegerField(
        null=True,
        help_text="The index value is used to preserve sorting of elections, \
since multiple elections may occur in a year. A greater sort index \
corresponds to a more recent election."
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedCandidate(BaseScrapedModel):
    """
    A candidate for office scraped from the California Secretary of State's site.
    """
    name = models.CharField(
        verbose_name="candidate name",
        max_length=200
    )
    scraped_id = models.CharField(
        verbose_name="candidate identification number",
        max_length=7,
        blank=True,  # Some don't have IDs on the website
    )
    office_name = models.CharField(
        verbose_name="name of the office for which this candidate is running",
        max_length=100,
        blank=True
    )
    election = models.ForeignKey('CandidateScrapedElection', null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PropositionScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesspropositions` command.
    """
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedProposition(BaseScrapedModel):
    """
    A yes or no ballot measure for voters scraped from the California Secretary of State's site.
    """
    # Most of the time, this is a number, however,
    # it can be a bona fide name, e.g.
    # '2003 Recall Question'
    name = models.CharField(
        verbose_name="proposition name",
        max_length=200
    )
    scraped_id = models.CharField(
        verbose_name="proposition identification number",
        max_length=200
    )
    election = models.ForeignKey('PropositionScrapedElection', null=True)

    class Meta:
        """
        Model options.
        """
        ordering = ("-election", "name")

    def __str__(self):
        return 'Proposition: {}'.format(self.name)


class BaseScrapedCommittee(BaseScrapedModel):
    """
    An committee scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for committees
    scraped as part of the candidates scraper, and one for committees scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        verbose_name="committee name",
        max_length=500
    )
    scraped_id = models.CharField(
        verbose_name="committee identification number",
        max_length=7
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class ScrapedPropositionCommittee(BaseScrapedCommittee):
    """
    A committee supporting or opposing a proposition scraped from the California Secretary of State's site.
    """
    position = models.CharField(
        max_length=100,
        help_text="Whether the committee supports or opposes the proposition",
    )
    proposition = models.ForeignKey('ScrapedProposition')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedCandidateCommittee(BaseScrapedCommittee):
    """
    A candidate committee scraped from the California Secretary of State's site.
    """
    candidate_id = models.CharField(
        max_length=100
    )
    status = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name