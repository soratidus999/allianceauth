import logging
import os

from allianceauth.authentication.models import CharacterOwnership, UserProfile
from bravado.exception import HTTPForbidden
from django.db import models
from esi.errors import TokenError
from esi.models import Token
from allianceauth.eveonline.models import EveCorporationInfo, EveCharacter
from allianceauth.notifications import notify

from allianceauth.corputils.managers import CorpStatsManager

SWAGGER_SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'swagger.json')

logger = logging.getLogger(__name__)


class CorpStats(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    corp = models.OneToOneField(EveCorporationInfo, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('view_corp_corpstats', 'Can view corp stats of their corporation.'),
            ('view_alliance_corpstats', 'Can view corp stats of members of their alliance.'),
            ('view_state_corpstats', 'Can view corp stats of members of their auth state.'),
            ('view_all_corpstats', 'Can view all corp stats.'),
        )
        verbose_name = "corp stats"
        verbose_name_plural = "corp stats"

    objects = CorpStatsManager()

    def __str__(self):
        return "%s for %s" % (self.__class__.__name__, self.corp)

    def update(self):
        try:
            c = self.token.get_esi_client(spec_file=SWAGGER_SPEC_PATH)

            # make sure the token owner is still in this corp
            assert c.Character.get_characters_character_id(character_id=self.token.character_id).result()[
                       'corporation_id'] == int(self.corp.corporation_id)

            # get member tracking data and retrieve member ids for translation
            tracking = c.Corporation.get_corporations_corporation_id_membertracking(corporation_id=self.corp.corporation_id).result()
            member_ids = [t['character_id'] for t in tracking]

            # requesting too many ids per call results in a HTTP400
            # the swagger spec doesn't have a maxItems count
            # manual testing says we can do over 350, but let's not risk it
            member_id_chunks = [member_ids[i:i + 255] for i in range(0, len(member_ids), 255)]
            member_name_chunks = [c.Character.get_characters_names(character_ids=id_chunk).result() for id_chunk in
                                  member_id_chunks]
            member_list = {t['character_id']: t for t in tracking}
            for name_chunk in member_name_chunks:
                for name in name_chunk:
                    member_list[name['character_id']].update(name)

            # get ship and location names
            for t in tracking:
                t['ship_type_name'] = c.Universe.get_universe_types_type_id(type_id=t['ship_type_id']).result()['name']
                locations = c.Universe.post_universe_names(ids=[t['location_id']]).result()
                t['location_name'] = locations[0]['name'] if locations else ''  # might be a citadel we can't know about
                member_list[t['character_id']].update(t)

            # purge old members
            self.members.exclude(character_id__in=member_ids).delete()

            # bulk update and create new member models
            for c_id, data in member_list.items():
                ownership = CharacterOwnership.objects.filter(character__character_id=c_id)
                data['registered'] = ownership.exists()
                if data['registered']:
                    owner = ownership[0]
                    data['main_character'] = owner.user.profile.main_character
                    alts = EveCharacter.objects.filter(character_ownership__user=owner.user)
                else:
                    data['main_character'] = None
                    alts = []
                if data['main_character']:
                    data['is_main'] = data['character_id'] == int(data['main_character'].character_id)
                    alts = alts.exclude(pk=data['main_character'].pk)
                else:
                    data['is_main'] = False
                member, _ = CorpMember.objects.update_or_create(character_id=c_id, corpstats=self, defaults=data)
                member.alts.set(alts)

            # update the timer
            self.save()

        except TokenError as e:
            logger.warning("%s failed to update: %s" % (self, e))
            if self.token.user:
                notify(self.token.user, "%s failed to update with your ESI token." % self,
                       message="Your token has expired or is no longer valid. Please add a new one to create a new CorpStats.",
                       level="error")
            self.delete()
        except HTTPForbidden as e:
            logger.warning("%s failed to update: %s" % (self, e))
            if self.token.user:
                notify(self.token.user, "%s failed to update with your ESI token." % self,
                       message="%s: %s" % (e.status_code, e.message), level="error")
            self.delete()
        except AssertionError:
            logger.warning("%s token character no longer in corp." % self)
            if self.token.user:
                notify(self.token.user, "%s cannot update with your ESI token." % self,
                       message="%s cannot update with your ESI token as you have left corp." % self, level="error")
            self.delete()

    @property
    def member_count(self):
        return self.members.count()

    @property
    def user_count(self):
        return self.members.filter(main_character__corporation_id=self.corp.corporation_id).count()

    @property
    def registered_member_count(self):
        return self.registered_members.count()

    @property
    def registered_members(self):
        return self.members.filter(registered=True)

    @property
    def unregistered_member_count(self):
        return self.unregistered_members.count()

    @property
    def unregistered_members(self):
        return self.members.filter(registered=False)

    @property
    def main_count(self):
        return self.mains.count()

    @property
    def alts(self):
        return EveCharacter.objects.filter(alt_corpmembers__corpstats=self)

    @property
    def alt_count(self):
        return self.alts.count()

    @property
    def mains(self):
        return self.members.filter(is_main=True)

    def visible_to(self, user):
        return CorpStats.objects.filter(pk=self.pk).visible_to(user).exists()

    def corp_logo(self, size=128):
        return "https://image.eveonline.com/Corporation/%s_%s.png" % (self.corp.corporation_id, size)

    def alliance_logo(self, size=128):
        if self.corp.alliance_id:
            return "https://image.eveonline.com/Alliance/%s_%s.png" % (self.corp.alliance_id, size)
        else:
            return "https://image.eveonline.com/Alliance/1_%s.png" % size


class CorpMember(models.Model):
    character_id = models.PositiveIntegerField()
    character_name = models.CharField(max_length=37)  # allegedly

    location_id = models.PositiveIntegerField()
    location_name = models.CharField(max_length=78)  # this was counted

    ship_type_id = models.PositiveIntegerField()
    ship_type_name = models.CharField(max_length=42)  # this was also counted

    start_date = models.DateTimeField()
    logon_date = models.DateTimeField()
    logoff_date = models.DateTimeField()

    base_id = models.PositiveIntegerField(blank=True, null=True)

    main_character = models.ForeignKey(EveCharacter, blank=True, null=True, on_delete=models.SET_NULL)
    alts = models.ManyToManyField(EveCharacter, blank=True, related_name='alt_corpmembers')
    registered = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)

    corpstats = models.ForeignKey(CorpStats, on_delete=models.CASCADE, related_name='members')

    class Meta:
        # not making character_id unique in case a character moves between two corps while only one updates
        unique_together = ('corpstats', 'character_id')
        ordering = ['character_name']

    def __str__(self):
        return self.character_name

    def portrait_url(self, size=32):
        return "https://image.eveonline.com/Character/%s_%s.jpg" % (self.character_id, size)

    def __getattr__(self, item):
        if item.startswith('portrait_url_'):
            size = item.strip('portrait_url_')
            return self.portrait_url(size)
        return self.__getattribute__(item)
