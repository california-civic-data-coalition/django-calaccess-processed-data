# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 20:20
from __future__ import unicode_literals

import calaccess_processed.models.proxies.opencivicdata.base
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_post_maximum_memberships'),
        ('elections', '0002_auto_20170731_2047'),
        ('calaccess_processed', '0002_auto_20170809_1539'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OCDRunoffProxy',
        ),
        migrations.CreateModel(
            name='OCDCandidateContestProxy',
            fields=[
            ],
            options={
                # 'indexes': [],
                'proxy': True,
            },
            bases=('elections.candidatecontest', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDMembershipProxy',
            fields=[
            ],
            options={
                # 'indexes': [],
                'proxy': True,
            },
            bases=('core.membership', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDOrganizationIdentifierProxy',
            fields=[
            ],
            options={
                # 'indexes': [],
                'proxy': True,
            },
            bases=('core.organizationidentifier', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDOrganizationNameProxy',
            fields=[
            ],
            options={
                # 'indexes': [],
                'proxy': True,
            },
            bases=('core.organizationname', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDPersonNameProxy',
            fields=[
            ],
            options={
                # 'indexes': [],
                'proxy': True,
            },
            bases=('core.personname', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
    ]
