import random

import factory.fuzzy
from factory.django import DjangoModelFactory

from core.users.factories import UserFactory
from apps.jobs import models


class TagFactory(DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.Sequence(lambda n: "name-tag#%d" % n)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: "name-category#%d" % n)
    public_name = factory.Sequence(lambda n: "public_name-category#%d" % n)

    type = factory.fuzzy.FuzzyChoice(models.Type)
    tag = factory.LazyAttribute(lambda _: TagFactory())


class FilterFactory(DjangoModelFactory):
    class Meta:
        model = models.Filter

    name = factory.Sequence(lambda n: "name-filter#%d" % n)
    public_name = factory.Sequence(lambda n: "public_name-filter#%d" % n)

    category = factory.LazyAttribute(lambda _: CategoryFactory())


class SDModelFactory(DjangoModelFactory):
    class Meta:
        model = models.SDModel

    id = factory.Sequence(lambda n: random.randint(1000, 9999))
    name = factory.Sequence(lambda n: "name-sd_model#%d" % n)
    public_name = factory.Sequence(lambda n: "public_name-sd_model#%d" % n)
    type = factory.fuzzy.FuzzyChoice(models.Type)


class ActionFactory(DjangoModelFactory):
    class Meta:
        model = models.Action

    id = factory.Faker('pyint')
    name = factory.Sequence(lambda n: "name-action#%d" % n)
    public_name = factory.Sequence(lambda n: "public_name-action#%d" % n)

    sd_model = factory.LazyAttribute(lambda _: SDModelFactory())
    type = factory.fuzzy.FuzzyChoice(models.Type)


class UndressJobFactory(DjangoModelFactory):
    class Meta:
        model = models.UndressJob

    user_id = factory.LazyAttribute(lambda _: UserFactory().id)
    sd_model = factory.LazyAttribute(lambda _: SDModelFactory())
    action = factory.LazyAttribute(lambda _: ActionFactory())
    estimated_time = 600
    time_spent = 10

    @factory.post_generation
    def filters(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.filters.add(*extracted)


class GenerateJobFactory(DjangoModelFactory):
    class Meta:
        model = models.GenerateJob

    user_id = factory.LazyAttribute(lambda _: UserFactory().id)
    sd_model = factory.SubFactory(SDModelFactory)
    action = factory.SubFactory(ActionFactory)

    @factory.post_generation
    def filters(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.filters.add(*extracted)


class ImageGalleryFactory(DjangoModelFactory):
    class Meta:
        model = models.ImageGallery

    job = factory.SubFactory(GenerateJobFactory)


class InstagramUndressJobFactory(DjangoModelFactory):
    class Meta:
        model = models.InstagramUndressJob

    user_id = factory.LazyAttribute(lambda _: UserFactory().id)
    link = factory.Faker('url')
    link_type = factory.fuzzy.FuzzyChoice(models.InstagramUndressJob.LinkType)


class InstagramSourceFactory(DjangoModelFactory):
    class Meta:
        model = models.InstagramSource

    job = factory.SubFactory(InstagramUndressJobFactory)
    image_url = factory.Faker('url')
