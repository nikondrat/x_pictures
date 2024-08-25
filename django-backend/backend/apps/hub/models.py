from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


class AbstractFilterModel(models.Model):
    id = models.CharField(_('ID'), primary_key=True, max_length=50)
    name = models.CharField(_('Name'), unique=True, max_length=50)
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


"""
Category: Base
"""


class FilterModel(AbstractFilterModel):
    """Category: Base | ForeignKey"""
    class Meta:
        db_table = 'hub_base__filter_model'
        verbose_name = _('Filter model')
        verbose_name_plural = _('Filter models')


class FilterNumberOfPeople(AbstractFilterModel):
    """Category: Base | ForeignKey"""
    class Meta:
        db_table = 'hub_base__filter_number_of_people'
        verbose_name = _('Filter number of people')
        verbose_name_plural = _('Filter number of peoples')


class FilterAge(AbstractFilterModel):
    """Category: Base | ForeignKey"""
    class Meta:
        db_table = 'hub_base__filter_age'
        verbose_name = _('Filter age')
        verbose_name_plural = _('Filter ages')


class FilterEthnicity(AbstractFilterModel):
    """Category: Base | ForeignKey"""
    class Meta:
        db_table = 'hub_base__filter_ethnicity'
        verbose_name = _('Filter ethnicity')
        verbose_name_plural = _('Filter ethnicities')


"""
Category: Body
"""


class FilterBodyType(AbstractFilterModel):
    """Category: Body | ForeignKey"""
    class Meta:
        db_table = 'hub_body__filter_body_type'
        verbose_name = _('Filter body type')
        verbose_name_plural = _('Filter body types')


class FilterSkin(AbstractFilterModel):
    """Category: Body | ManyToManyField"""
    class Meta:
        db_table = 'hub_body__filter_skin'
        verbose_name = _('Filter skin')
        verbose_name_plural = _('Filter skins')


class FilterBreast(AbstractFilterModel):
    """Category: Body | ForeignKey"""
    class Meta:
        db_table = 'hub_body__filter_breast'
        verbose_name = _('Filter breast')
        verbose_name_plural = _('Filter breasts')


class FilterAss(AbstractFilterModel):
    """Category: Body | ForeignKey"""
    class Meta:
        db_table = 'hub_body__filter_ass'
        verbose_name = _('Filter ass')
        verbose_name_plural = _('Filter asses')


"""
Category: Face
"""


class FilterFace(AbstractFilterModel):
    """Category: Face | ManyToManyField"""
    class Meta:
        db_table = 'hub_face__filter_face'
        verbose_name = _('Filter face')
        verbose_name_plural = _('Filter faces')


class FilterHairColor(AbstractFilterModel):
    """Category: Face | ManyToManyField"""
    class Meta:
        db_table = 'hub_face__filter_hair_color'
        verbose_name = _('Filter hair color')
        verbose_name_plural = _('Filter hair colors')


class FilterHairType(AbstractFilterModel):
    """Category: Face | ManyToManyField"""
    class Meta:
        db_table = 'hub_face__filter_hair_type'
        verbose_name = _('Filter hair type')
        verbose_name_plural = _('Filter hair types')


"""
Category: Clothes
"""


class FilterClothes(AbstractFilterModel):
    """Category: Clothes | ManyToManyField"""
    class Meta:
        db_table = 'hub_clothes__filter_clothes'
        verbose_name = _('Filter clothes')
        verbose_name_plural = _('Filter clothes')


class FilterClothModifier(AbstractFilterModel):
    """Category: Clothes | ManyToManyField"""
    class Meta:
        db_table = 'hub_clothes__filter_cloth_modifier'
        verbose_name = _('Filter cloth modifier')
        verbose_name_plural = _('Filter cloth modifiers')


"""
Category: Style
"""


class FilterDistance(AbstractFilterModel):
    """Category: Style | ForeignKey"""
    class Meta:
        db_table = 'hub_style__filter_distance'
        verbose_name = _('Filter distance')
        verbose_name_plural = _('Filter distances')


class FilterAngle(AbstractFilterModel):
    """Category: Style | ForeignKey"""
    class Meta:
        db_table = 'hub_style__filter_angle'
        verbose_name = _('Filter angle')
        verbose_name_plural = _('Filter angles')


class FilterAction(AbstractFilterModel):
    """Category: Style | ForeignKey"""
    class Meta:
        db_table = 'hub_style__filter_action'
        verbose_name = _('Filter action')
        verbose_name_plural = _('Filter actions')


class FilterSetting(AbstractFilterModel):
    """Category: Style | ManyToManyField"""
    class Meta:
        db_table = 'hub_style__filter_setting'
        verbose_name = _('Filter setting')
        verbose_name_plural = _('Filter settings')


class FilterLight(AbstractFilterModel):
    """Category: Style | ManyToManyField"""
    class Meta:
        db_table = 'hub_style__filter_light'
        verbose_name = _('Filter light')
        verbose_name_plural = _('Filter lights')


class FilterStyle(AbstractFilterModel):
    """Category: Style | ManyToManyField"""
    class Meta:
        db_table = 'hub_style__filter_style'
        verbose_name = _('Filter style')
        verbose_name_plural = _('Filter styles')


"""
Main models
"""


class AiModel(AbstractFilterModel):
    preview_image_url = models.URLField(_('Preview image url'), null=True, blank=True, default=None)

    class Meta:
        db_table = 'hub_ai_model'
        verbose_name = _('Ai model')
        verbose_name_plural = _('Ai models')


class PornAction(AbstractFilterModel):
    preview_image_url = models.URLField(_('Preview image url'), null=True, blank=True, default=None)

    class Meta:
        db_table = 'hub_porn_action'
        verbose_name = _('Porn action')
        verbose_name_plural = _('Porn actions')


class ImageHub(models.Model):
    image_url = models.URLField(_('Image URL'), default=None, null=True)

    filter_model = models.ForeignKey(FilterModel, verbose_name=_('Filter model'), null=True, blank=True, default=None,
                                     related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_number_of_people = models.ForeignKey(FilterNumberOfPeople, verbose_name=_('Filter number of people'),
                                                null=True, blank=True, default=None, related_name='images_hub',
                                                on_delete=models.SET_DEFAULT)
    filter_age = models.ForeignKey(FilterAge, verbose_name=_('Filter age'), null=True, blank=True, default=None,
                                   related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_ethnicity = models.ForeignKey(FilterEthnicity, verbose_name=_('Filter ethnicity'), null=True, blank=True,
                                         default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)

    filter_body_type = models.ForeignKey(FilterBodyType, verbose_name=_('Filter body type'), null=True, blank=True,
                                         default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_skin = models.ManyToManyField(FilterSkin, verbose_name=_('Filter skin'), related_name='images_hub',
                                         blank=True)
    filter_breast = models.ForeignKey(FilterBreast, verbose_name=_('Filter breast'), null=True, blank=True,
                                      default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_ass = models.ForeignKey(FilterAss, verbose_name=_('Filter ass'), null=True, blank=True,
                                   default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)

    filter_face = models.ManyToManyField(FilterFace, verbose_name=_('Filter face'), related_name='images_hub',
                                         blank=True)
    filter_hair_color = models.ManyToManyField(FilterHairColor, verbose_name=_('Filter hair color'),
                                               related_name='images_hub', blank=True)
    filter_hair_type = models.ManyToManyField(FilterHairType, verbose_name=_('Filter hair type'),
                                              related_name='images_hub', blank=True)

    filter_clothes = models.ManyToManyField(FilterClothes, verbose_name=_('Filter clothes'), related_name='images_hub',
                                            blank=True)
    filter_cloth_modifier = models.ManyToManyField(FilterClothModifier, verbose_name=_('Filter cloth modifier'),
                                                   related_name='images_hub', blank=True)

    filter_distance = models.ForeignKey(FilterDistance, verbose_name=_('Filter distance'), null=True, blank=True,
                                        default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_angle = models.ForeignKey(FilterAngle, verbose_name=_('Filter angle'), null=True, blank=True,
                                     default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_action = models.ForeignKey(FilterAction, verbose_name=_('Filter action'), null=True, blank=True,
                                      default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)
    filter_setting = models.ManyToManyField(FilterSetting, verbose_name=_('Filter setting'), related_name='images_hub',
                                            blank=True)
    filter_light = models.ManyToManyField(FilterLight, verbose_name=_('Filter light'), related_name='images_hub',
                                          blank=True)
    filter_style = models.ManyToManyField(FilterStyle, verbose_name=_('Filter style'), related_name='images_hub',
                                          blank=True)

    ai_model = models.ForeignKey(AiModel, verbose_name=_('Ai model'), null=True, blank=True,
                                 default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)

    porn_action = models.ForeignKey(PornAction, verbose_name=_('Porn action'), null=True, blank=True,
                                    default=None, related_name='images_hub', on_delete=models.SET_DEFAULT)

    show_in_hub = models.BooleanField(_('Show in hub'), default=True)

    class Meta:
        db_table = 'hub_images'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f'{self.image_url}'

    @property
    def preview_image(self):
        return mark_safe(f'<img src="{self.image_url}" width="50" height="50" />')

    @property
    def image(self):
        return mark_safe(f'<img src="{self.image_url}" />')

    @property
    def prompt(self) -> str:
        return ''
