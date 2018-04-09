from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.management import create_permissions

import logging

logger = logging.getLogger(__name__)


def migrate_service_enabled(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None
        
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    MediawikiUser = apps.get_model("mediawiki", "MediawikiUser")

    perm = Permission.objects.get(codename='access_mediawiki')

    member_group_name = getattr(settings, str('DEFAULT_AUTH_GROUP'), 'Member')
    blue_group_name = getattr(settings, str('DEFAULT_BLUE_GROUP'), 'Blue')

    # Migrate members
    if MediawikiUser.objects.filter(user__groups__name=member_group_name).exists() or \
            getattr(settings, str('ENABLE_AUTH_MEDIAWIKI'), False):
        try:
            group = Group.objects.get(name=member_group_name)
            group.permissions.add(perm)
        except ObjectDoesNotExist:
            logger.warning('Failed to migrate ENABLE_AUTH_MEDAIWIKI setting')

    # Migrate blues
    if MediawikiUser.objects.filter(user__groups__name=blue_group_name).exists() or \
            getattr(settings, str('ENABLE_BLUE_MEDIAWIKI'), False):
        try:
            group = Group.objects.get(name=blue_group_name)
            group.permissions.add(perm)
        except ObjectDoesNotExist:
            logger.warning('Failed to migrate ENABLE_BLUE_MEDIAWIKI setting')


class Migration(migrations.Migration):

    dependencies = [
        ('mediawiki', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediawikiuser',
            options={'permissions': (('access_mediawiki', 'Can access the Mediawiki service'),)},
        ),
        migrations.RunPython(migrate_service_enabled),
    ]
