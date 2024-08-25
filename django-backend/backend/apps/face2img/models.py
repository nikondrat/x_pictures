import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.users.models import User
from core.common.utils import PathAndRename


class Pack(models.Model):
    class Category(models.TextChoices):
        LINKED_IN = 'LinkedIn', _('LinkedIn')
        HAIR_STYLE = 'Hair style', _('Hair style')
        SMART_TOOL = 'Smart tool', _('Smart tool')
        TRAVEL = 'Travel', _('Travel')
        CLASSY = 'Classy', _('Classy')
        FASHION = 'Fashion', _('Fashion')
        DECADES_TRANSFORMATIONS = 'Decades transformations', _('Decades transformations')
        MOVIES = 'Movies', _('Movies')
        Y2K = 'Y2K', _('Y2K')
        ACTIVITIES = 'Activities', _('Activities')
        SUIT = 'Suit', _('Suit')
        OFFICE = 'Office', _('Office')
        CASUAL = 'Casual', _('Casual')
        BUSINESS = 'Business', _('Business')
        BLACK_BACKGROUND = 'Black background', _('Black background')
        WHITE_BACKGROUND = 'White background', _('White background')
        CASUAL_SELFIE = 'Casual selfie', _('Casual selfie')
        BOB_CUT = 'Bob cut', _('Bob cut')
        COLORFUL_HAIR = 'Colorful hair', _('Colorful hair')
        BROWN_HAIR = 'Brown hair', _('Brown hair')
        BUZZ_CUT = 'Buzz cut', _('Buzz cut')
        CURLY = 'Curly', _('Curly')
        GINGER = 'Ginger', _('Ginger')
        OLD_MONEY = 'Old money', _('Old money')
        BEACH = 'Beach', _('Beach')
        BLOND = 'Blond', _('Blond')
        SANTORINI = 'Santorini', _('Santorini')
        EIFFEL_TOWER = 'Eiffel Tower', _('Eiffel Tower')
        BORA_BORA = 'Bora bora', _('Bora bora')
        GRAND_CANYON = 'Grand Canyon', _('Grand Canyon')
        CAPPADOCIA = 'Cappadocia', _('Cappadocia')
        NIAGARA_FALLS = 'Niagara Falls', _('Niagara Falls')
        ISTANBUL = 'Istanbul', _('Istanbul')
        CLINIQUE_YERDE = 'Clinique yerde', _('Clinique yerde')
        TAK_MAHAL = 'Tak mahal', _('Tak mahal')
        COLESSEUM = 'Colesseum', _('Colesseum')
        MONACO = 'Monaco', _('Monaco')
        VENICE = 'Venice', _('Venice')
        MALDIVES = 'Maldives', _('Maldives')
        SYDNEY = 'Sydney', _('Sydney')
        HONG_KONG = 'Hong Kong', _('Hong Kong')
        JAPAN = 'Japan', _('Japan')
        DUBAI = 'Dubai', _('Dubai')
        MILAN = 'Milan', _('Milan')
        SWITZERLAND = 'Switzerland', _('Switzerland')
        MUNICH = 'Munich', _('Munich')
        LUXURY = 'Luxury', _('Luxury')
        DATE = 'Date', _('Date')
        COFFEE_DATE = 'Coffee date', _('Coffee date')
        WEDDING = 'Wedding', _('Wedding')
        RED_CARPET = 'Red carpet', _('Red carpet')
        ELITE = 'Elite', _('Elite')
        YACHT = 'Yacht', _('Yacht')
        PRIVATE_JET = 'Private jet', _('Private jet')
        OPERA = 'Opera', _('Opera')
        PODIUM = 'Podium', _('Podium')
        STUDIO_SHOOTING = 'Studio shooting', _('Studio shooting')
        STREET_STYLE = 'Street style', _('Street style')
        LOOK_BOOK = 'Look book', _('Look book')
        BLACK_AND_WHITE = 'Black & white', _('Black & white')
        THE_1940S = 'The 1940s', _('The 1940s')
        THE_1950S = 'The 1950s', _('The 1950s')
        THE_1960S = 'The 1960s', _('The 1960s')
        THE_1970S = 'The 1970s', _('The 1970s')
        THE_1980S_ARCADE = 'The 1980s arcade', _('The 1980s arcade')
        THE_1980S = 'The 1980s', _('The 1980s')
        THE_1990S = 'The 1990s', _('The 1990s')
        THE_2000S = 'The 2000s', _('The 2000s')
        MONOCHROME_POLAROID = 'Monochrome Polaroid', _('Monochrome Polaroid')
        POLAROID = 'Polaroid', _('Polaroid')
        THE_WALKING_DEAD = 'The walking dead', _('The walking dead')
        THE_HUNGER_GAMES = 'The hunger games', _('The hunger games')
        AVATAR = 'Avatar', _('Avatar')
        MARVEL = 'Marvel', _('Marvel')
        SUICIDE_SQUAD = 'Suicide Squad', _('Suicide Squad')
        GAME_OF_THRONES = 'Game of Thrones', _('Game of Thrones')
        BREAKING_BAD = 'Breaking bad', _('Breaking bad')
        FRIENDS = 'Friends', _('Friends')
        DESPERATE_HOUSEWIVES = 'Desperate housewives', _('Desperate housewives')
        THE_LAST_OF_US = 'The last of us', _('The last of us')
        YVES_SAINT_LAURENT = 'Yves Saint Laurent', _('Yves Saint Laurent')
        BURBERRY = 'Burberry', _('Burberry')
        DIOR = 'Dior', _('Dior')
        PRADA = 'Prada', _('Prada')
        CHANEL = 'Chanel', _('Chanel')
        HERMES = 'Hermes', _('Hermes')
        LOUIS_VUITTON = 'Louis Vuitton', _('Louis Vuitton')
        CHLOE = 'Chloe', _('Chloe')
        ATHLETE = 'Athlete', _('Athlete')
        GOTH = 'Goth', _('Goth')
        NERD = 'Nerd', _('Nerd')
        PROM_SKATER = 'Prom skater', _('Prom skater')
        HIP_HOP = 'Hip hop', _('Hip hop')
        HORSE_RIDING = 'Horse riding', _('Horse riding')
        TENNIS = 'Tennis', _('Tennis')
        GOLF = 'Golf', _('Golf')


    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), null=True, blank=True)
    category = models.CharField(_("Category"), max_length=255, choices=Category.choices, default=Category.SMART_TOOL)

    sd_model = models.CharField(_("SD model"), max_length=255)
    positive_prompt = models.CharField(_("Prompt"), max_length=255)
    negative_prompt = models.CharField(_("Negative prompt"), max_length=255)

    image_default_height = models.IntegerField(_("Height"), default=768)
    image_default_width = models.IntegerField(_("Height"), default=512)
    steps = models.IntegerField(_("Steps"), default=20)
    batch_size = models.IntegerField(_("Batch size"), default=4)
    sampler_name = models.CharField(_("Sampler name"), max_length=255)

    is_active = models.BooleanField(_("Is active"), default=True)

    class Meta:
        verbose_name = _('Pack')
        verbose_name_plural = _('Packs')

    def __str__(self):
        return self.name


class PackImage(models.Model):
    pack = models.ForeignKey(Pack, verbose_name=_("Pack"), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        _("Image"),
        upload_to=PathAndRename('face2img_packs_default_images/'),
        null=True,
        blank=True,
    )
    sort = models.IntegerField(_("Sort"), default=0)

    class Meta:
        verbose_name = _('Pack Image')
        verbose_name_plural = _('Pack Images')


class Lora(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        PROCESS = 1, _('Process')
        SUCCESS = 2, _('Success')
        ERROR = -1, _('Error')

    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4)
    lora_name = models.CharField(_("Lora name"), max_length=255)
    train_task_id = models.CharField(_("Train task ID"), max_length=255, null=True, blank=True)
    train_model_name = models.CharField(_("Train model name"), max_length=255, null=True, blank=True)

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='loras')

    status = models.IntegerField(_("Status"), choices=Status.choices, default=Status.CREATED)

    estimated_time = models.IntegerField(_('Estimated time'), default=60, help_text=_('In second'))
    training_time_seconds = models.IntegerField(_("Training time"), null=True, blank=True)

    cost = models.DecimalField(_('Cost'), max_digits=25, decimal_places=2, default=0)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('User Lora')
        verbose_name_plural = _('User Loras')


class LoraTrainingFace(models.Model):
    lora = models.ForeignKey(Lora, verbose_name=_("Lora"), on_delete=models.CASCADE, related_name='training_faces')
    image = models.ImageField(
        _("Image"),
        upload_to=PathAndRename('face2img_lora_training_faces/'),
        null=True,
        blank=True,
    )

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('Lora Training Face')
        verbose_name_plural = _('Lora Training Faces')


class Face2ImgJob(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0, _('Created')
        PROCESS = 1, _('Process')
        SUCCESS = 2, _('Success')
        ERROR = -1, _('Error')

    id = models.UUIDField(_('ID'), primary_key=True, default=uuid.uuid4)

    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, related_name='face2img_jobs')
    lora = models.ForeignKey(Lora, verbose_name=_("Lora"), on_delete=models.CASCADE, related_name='jobs')
    pack = models.ForeignKey(Pack, verbose_name=_("Pack"), on_delete=models.CASCADE, related_name='jobs')

    status = models.IntegerField(_("Status"), choices=Status.choices, default=Status.CREATED)

    estimated_time = models.IntegerField(_('Estimated time'), default=60, help_text=_('In second'))
    time_spent = models.IntegerField(_('Time spent'), default=0, help_text=_('In seconds'))

    cost = models.DecimalField(_('Cost'), max_digits=25, decimal_places=2, default=0)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('Face2Img Job')
        verbose_name_plural = _('Face2Img Jobs')


class Face2ImgJobResult(models.Model):
    job = models.ForeignKey(Face2ImgJob, verbose_name=_("Job"), on_delete=models.CASCADE, related_name='results')
    image = models.ImageField(_("Image"), upload_to=PathAndRename('face2img/job_results/'), null=True, blank=True)

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Created'), auto_now=True)

    class Meta:
        verbose_name = _('Job Result')
        verbose_name_plural = _('Job Results')
