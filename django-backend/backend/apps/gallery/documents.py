from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.jobs.models import GenerateJob, Filter, SDModel, Action
# from apps.jobs.models import VideoJob


@registry.register_document
class GenerateJobDocument(Document):
    sd_model = fields.ObjectField(properties={
        'pk': fields.IntegerField(),
        'public_name': fields.TextField(),
    })
    action = fields.ObjectField(properties={
        'pk': fields.IntegerField(),
        'public_name': fields.TextField(),
    })
    filters = fields.ObjectField(properties={
        'pk': fields.IntegerField(),
        'public_name': fields.TextField(),
    })

    class Index:
        name = 'image_gallery'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = GenerateJob
        fields = [
            'id',
        ]
        related_models = [Filter, SDModel, Action]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'sd_model',
            'action',
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Filter):
            return related_instance.generatejob_set.all()
        elif isinstance(related_instance, Action):
            return related_instance.generatejob_set.all()
        elif isinstance(related_instance, SDModel):
            return related_instance.generatejob_set.all()


# @registry.register_document
# class VideoJobDocument(Document):
#     sd_model = fields.ObjectField(properties={
#         'pk': fields.IntegerField(),
#         'public_name': fields.TextField(),
#     })
#     filters = fields.ObjectField(properties={
#         'pk': fields.IntegerField(),
#         'public_name': fields.TextField(),
#     })
#
#     class Index:
#         name = 'video_gallery'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0,
#         }
#
#     class Django:
#         model = VideoJob
#         fields = [
#             'id',
#         ]
#         related_models = [Filter, SDModel]
#
#     def get_queryset(self):
#         return super().get_queryset().select_related(
#             'sd_model',
#         )
#
#     def get_instances_from_related(self, related_instance):
#         if isinstance(related_instance, Filter):
#             return related_instance.generatejob_set.all()
#         elif isinstance(related_instance, SDModel):
#             return related_instance.generatejob_set.all()
