import decimal
from typing import Optional

from django.conf import settings
from django.db import transaction

from core.common.cached.ram import Cached
from core.users.models import User
from apps.jobs.models import GenerateJob, ProxyGenerateJob
from apps.jobs.models import SDModel, Action, Filter
from apps.jobs.core.base import BaseService

QUEUES = {
    1: 'gen_free_queue',
    3: 'gen_basic_queue',
    5: 'gen_advance_queue',
    8: 'gen_premium_queue',
    10: 'gen_super_premium_queue',
}


class PromptEngin:

    @classmethod
    def _build_headers(cls, sd_model: SDModel, action: Action):
        lora_name = '' if action.pk == 2 else f'{action.lora_name}, '
        return f'{lora_name}{sd_model.raw_prompt} '

    @classmethod
    def _build_block1_age_and_model(cls, age: Filter, model: Filter):
        params_id9 = {
            15: ('18 y.o. ', 'girl '),
            16: ('25 y.o. ', 'woman '),
            17: ('45 y.o. ', 'milf '),
            18: ('65+ y.o. ', 'granny ')
        }
        params_id10 = {
            15: ('18 y.o. ', 'guy '),
            16: ('25 y.o. ', 'man '),
            17: ('45 y.o. ', 'man '),
            18: ('65+ y.o. ', 'grandfather ')
        }
        params_id11 = {
            15: ('18 y.o. ', 'transgender '),
            16: ('25 y.o. ', 'transgender '),
            17: ('45 y.o. ', 'transgender '),
            18: ('65+ y.o. ', 'transgender ')
        }

        builder_func = {
            9: params_id9,
            10: params_id10,
            11: params_id11,
        }
        return builder_func[model.pk][age.pk]

    @classmethod
    def _build_block1_age_and_model_many(cls, age: Filter, model: Filter):
        params_id9 = {
            15: ('18 y.o. ', 'girls '),
            16: ('25 y.o. ', 'women '),
            17: ('45 y.o. ', 'milfs '),
            18: ('65+ y.o. ', 'Granny ')
        }
        params_id10 = {
            15: ('18 y.o. ', 'boys '),
            16: ('25 y.o. ', 'men '),
            17: ('45 y.o. ', 'men '),
            18: ('65+ y.o. ', 'grandfathers ')
        }

        params_id11 = {
            15: ('18 y.o. ', 'transgenders '),
            16: ('25 y.o. ', 'transgenders '),
            17: ('45 y.o. ', 'transgenders '),
            18: ('65+ y.o. ', 'transgenders ')
        }

        builder_func = {
            9: params_id9,
            10: params_id10,
            11: params_id11,
        }
        return builder_func[model.pk][age.pk]

    @classmethod
    def _build_block1(cls, action: Action, filters: list[Filter]):
        number_or_people, age, model, ethnicity = '', '', '', ''
        lora_raw_prompt = '' if action.pk == 2 else f'{action.raw_prompt1}, '

        age_obj = None
        model_obj = None
        number_or_people_obj = None

        new_filters = []
        for fil in filters:
            if fil.category.pk == 4:
                number_or_people_obj = fil
                number_or_people = f'{fil.raw_prompt} '
            elif fil.category.pk == 5:
                age_obj = fil
                age = f'{fil.raw_prompt} age '
            elif fil.category.pk == 3:
                model_obj = fil
                model = f'{fil.raw_prompt} '
            elif fil.category.pk == 6:
                ethnicity = f'{fil.raw_prompt} '
            else:
                new_filters.append(fil)

        if age_obj and model_obj:
            if number_or_people_obj and number_or_people_obj.pk in [13, 14]:
                age, model = cls._build_block1_age_and_model_many(age=age_obj, model=model_obj)
            else:
                age, model = cls._build_block1_age_and_model(age=age_obj, model=model_obj)

        prompt = f'{number_or_people}{age}{ethnicity}{model}{lora_raw_prompt}'.rstrip(', ')
        if prompt:
            prompt += ', '

        return new_filters, prompt

    @classmethod
    def _build_block2(cls, filters: list[Filter]):
        clothes_type, hair_type, hair_color = '', '', ''
        new_filters = []
        for fil in filters:
            if fil.category.pk == 14:
                clothes_type = f'{fil.raw_prompt}, '
            elif fil.category.pk == 13:
                hair_type = f'{fil.raw_prompt}, '
            elif fil.category.pk == 12:
                hair_color = f'{fil.raw_prompt} hair color, '
            else:
                new_filters.append(fil)
        return new_filters, f'{clothes_type}{hair_type}{hair_color}'

    @classmethod
    def _build_block3(cls, action: Action, filters: list[Filter]):
        kwargs = ''
        body_type, skin, breast, ass = '', '', '', ''
        lora_raw_prompt = '' if action.pk == 2 else f'{action.raw_prompt2}, '

        for fil in filters:
            if fil.category.pk == 7:
                body_type = f'{fil.raw_prompt} body, '
            elif fil.category.pk == 8:
                skin = f'{fil.raw_prompt} skin, '
            elif fil.category.pk == 9:
                breast = f'{fil.raw_prompt} breast, '
            elif fil.category.pk == 10:
                ass = f'{fil.raw_prompt} ass, '
            else:
                kwargs += f'{fil.raw_prompt}, '

        kwargs = kwargs.rstrip(', ')
        prompt = f'{body_type}{skin}{breast}{ass}{kwargs} {lora_raw_prompt}'.rstrip(', ')
        if prompt:
            prompt += ', '

        return prompt

    @classmethod
    def build(cls, sd_model: SDModel, action: Action, filters: list[Filter]):
        header_prompt = cls._build_headers(sd_model=sd_model, action=action)
        clip_block1_to_block2 = '((correct anatomy)), ((correct body)), ((correct number of limbs)), '
        clip_block3_to_footer = 'beautiful'
        if filters:
            new_filters, prompt_block1 = cls._build_block1(action=action, filters=filters)
            new_filters, prompt_block2 = cls._build_block2(filters=new_filters)
            prompt_block3 = cls._build_block3(action=action, filters=new_filters)

            prompt = (f'{header_prompt}{prompt_block1}{clip_block1_to_block2}'
                      f'{prompt_block2}{prompt_block3}{clip_block3_to_footer}')
        else:
            prompt = f'f{header_prompt}one 25 y.o. german woman, {clip_block1_to_block2}{clip_block3_to_footer}'
        return prompt


class NegativePromptEngin:
    @classmethod
    def build(cls, sd_model: SDModel, action: Action, filters: list[Filter]):
        return ("(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, ((duplicate)), "
                "wrong anatomy, extra limb, missing limb, floating limbs, "
                "(mutated hands and fingers:1.4), disconnected limbs, mutation, "
                "mutated, (ugly), disgusting, blurry, amputation, ((blurry)), poorly drawn, words, boring, "
                "duplicate, (large areolae), extra fingers, mutated hands, cross-eye, (clone), "
                "mirror, ugly skin, artifacts, bad art, out of frame, lowres, text, error, cropped,ive legs, "
                "3 legs, three legs, five legs, 5 legs, bad hands, bad legs, bad body shape, multiple tails, "
                "two tails, deformated body, imperfect painting, blurry hands, blurry face, blurry body")


@Cached(timeout=60 * 30)
def generate_prompt(sd_model: SDModel, action: Action, filters: list[Filter]):
    prompt = PromptEngin.build(sd_model=sd_model, action=action, filters=filters)
    negative_prompt = NegativePromptEngin.build(sd_model=sd_model, action=action, filters=filters)
    return prompt, negative_prompt


class Service(BaseService):
    use_task = settings.USE_GENERATE_NOVITA

    rabbitmq_queue = settings.ML_GENERATE_QUEUE
    rabbitmq_routing_key = settings.ML_GENERATE_QUEUE

    task_name = 'jobs:create-generate:task'

    @classmethod
    @Cached(timeout=60 * 60)
    def get_ml_params(cls, filter_ids: list[int], sd_model_id: Optional[int] = None,
                      action_id: Optional[int] = None) -> dict:
        prompt, negative_prompt = generate_prompt(
            sd_model=SDModel.objects.get(pk=sd_model_id),
            action=Action.objects.get(pk=action_id),
            filters=Filter.objects.select_related('category').filter(pk__in=filter_ids)
        )
        return {
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'step': 20,
            'sampler_name': 'DPM++ 2M SDE Karras',
            'cfg_scale': 7,
        }

    @classmethod
    def get_queue_by_priority(cls, priority: int) -> str:
        return QUEUES[priority]

    @classmethod
    @transaction.atomic()
    def make_job(cls, user: User, filter_ids: list[int], cost: decimal.Decimal, **kwargs):
        params = cls.get_ml_params(
            filter_ids=filter_ids,
            sd_model_id=kwargs['sd_model_id'],
            action_id=kwargs['action_id']
        )

        profile = user_id = None
        if user.is_authenticated:
            user_id = user.pk
            profile = user.profile

        estimated_time = cls.get_estimated_time(profile=profile)
        need_blur = cls.get_need_blur(profile=profile, cost=cost)
        need_watermark = cls.get_need_watermark(profile=profile, cost=cost)
        priority = cls.get_priority(profile=profile)

        if profile and profile.balance >= cost:
            profile.balance -= cost
            profile.save()
        else:
            cost = 0

        job = GenerateJob.objects.create(
            user_id=user_id,
            sd_model_id=kwargs['sd_model_id'],
            action_id=kwargs['action_id'],
            positive_prompt=params['prompt'],
            negative_prompt=params['negative_prompt'],
            step=params['step'],
            sampler_name=params['sampler_name'],
            estimated_time=estimated_time,
            status=GenerateJob.Status.PROCESS,
            cost=cost,
            show_in_profile=user.is_authenticated,
            need_blur=need_blur,
            need_watermark=need_watermark,
        )
        job.filters.add(*filter_ids)
        job.save()

        transaction.on_commit(lambda: cls.make_request(
            correlation_id=job.pk,
            data={
                'sd_model': job.sd_model.model_name,
                'size': cls.get_size(profile=profile),
                'next_queue': cls.get_queue_by_priority(priority=priority),
                **params,
            },
            priority=priority,
        ))

        return job


class ProxyService(Service):

    @classmethod
    def get_fake_job(cls, job: GenerateJob) -> GenerateJob:
        proxy_job = ProxyGenerateJob.objects.create(
            job=job,
        )
        return proxy_job

    @classmethod
    @transaction.atomic()
    def make_job(cls, user: User, filter_ids: list[int], cost: decimal.Decimal, **kwargs):
        if user.is_anonymous:
            conf = cls.get_ml_params(
                filter_ids=filter_ids,
                sd_model_id=kwargs['sd_model_id'],
                action_id=kwargs['action_id'],
            )

            qs = GenerateJob.objects.exclude(
                id__in=ProxyGenerateJob.objects.values_list('pk', flat=True),
            ).filter(
                sd_model_id=kwargs['sd_model_id'],
                action_id=kwargs['action_id'],
                need_blur=True,
                status=GenerateJob.Status.SUCCESS,
                positive_prompt=conf['prompt'],
                negative_prompt=conf['negative_prompt'],
            )

            if job := qs.first():
                return cls.get_fake_job(job=job)

        return super().make_job(user=user, filter_ids=filter_ids, cost=cost, **kwargs)


class WhiteGenerate(Service):
    @classmethod
    @transaction.atomic()
    def make_job(cls, user: User, sd_model_id: int, prompt: str, negative_prompt: str, cost: decimal.Decimal):
        profile = user_id = None
        if user.is_authenticated:
            user_id = user.pk
            profile = user.profile

        estimated_time = cls.get_estimated_time(profile=profile)
        need_blur = cls.get_need_blur(profile=profile, cost=cost)
        need_watermark = cls.get_need_watermark(profile=profile, cost=cost)
        priority = cls.get_priority(profile=profile)

        if profile and profile.balance >= cost:
            profile.balance -= cost
            profile.save()
        else:
            cost = 0

        job = GenerateJob.objects.create(
            user_id=user_id,
            sd_model_id=sd_model_id,
            action_id=1,
            positive_prompt=prompt,
            negative_prompt=negative_prompt,
            step=20,
            sampler_name='DPM++ 2M SDE Karras',
            estimated_time=estimated_time,
            status=GenerateJob.Status.PROCESS,
            cost=cost,
            show_in_profile=user.is_authenticated,
            need_blur=need_blur,
            need_watermark=need_watermark,
        )
        job.save()

        transaction.on_commit(lambda: cls.make_request(
            correlation_id=job.pk,
            data={
                'sd_model': job.sd_model.model_name,
                'size': cls.get_size(profile=profile),
                'next_queue': cls.get_queue_by_priority(priority=priority),
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'step': 20,
                'sampler_name': 'DPM++ 2M SDE Karras',
                'cfg_scale': 7,
            },
            priority=priority,
        ))

        return job
