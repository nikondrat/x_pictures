# Generated by Django 3.2.22 on 2024-01-23

from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    Action = apps.get_model('jobs', 'Action')

    Action.objects.bulk_create([
        Action(id=33, name='Dildo (Photorealistic Generate)', public_name='Dildo', type=0, sd_model_id=2,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),
        Action(id=35, name='Dildo (Cartoon Generate)', public_name='Dildo', type=0, sd_model_id=3,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),
        Action(id=36, name='Dildo (Anime Generate)', public_name='Dildo', type=0, sd_model_id=4,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),
        Action(id=37, name='Dildo (Furry Generate)', public_name='Dildo', type=0, sd_model_id=5,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),
        Action(id=38, name='Dildo (3D Generate)', public_name='Dildo', type=0, sd_model_id=6,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),
        Action(id=39, name='Dildo (Art Generate)', public_name='Dildo', type=0, sd_model_id=7,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),
        Action(id=34, name='Dildo (Semi realism Generate)', public_name='Dildo', type=0, sd_model_id=8,
               lora_name='<lora:dildoVaginaV1:0.85>', raw_prompt1=''),

        Action(id=40, name='Cow girl (Photorealistic Generate)', public_name='Cow girl', type=0, sd_model_id=2,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),
        Action(id=41, name='Cow girl (Cartoon Generate)', public_name='Cow girl', type=0, sd_model_id=3,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),
        Action(id=42, name='Cow girl (Anime Generate)', public_name='Cow girl', type=0, sd_model_id=4,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),
        Action(id=43, name='Cow girl (Furry Generate)', public_name='Cow girl', type=0, sd_model_id=5,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),
        Action(id=44, name='Cow girl (3D Generate)', public_name='Cow girl', type=0, sd_model_id=6,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),
        Action(id=45, name='Cow girl (Art Generate)', public_name='Cow girl', type=0, sd_model_id=7,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),
        Action(id=46, name='Cow girl (Semi realism Generate)', public_name='Cow girl', type=0, sd_model_id=8,
               lora_name='<lora:cowGirlV1:1>', raw_prompt1=''),

        Action(id=47, name='Pov (Photorealistic Generate)', public_name='Pov', type=0, sd_model_id=2,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
        Action(id=48, name='Pov (Cartoon Generate)', public_name='Pov', type=0, sd_model_id=3,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
        Action(id=49, name='Pov (Anime Generate)', public_name='Pov', type=0, sd_model_id=4,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
        Action(id=50, name='Pov (Furry Generate)', public_name='Pov', type=0, sd_model_id=5,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
        Action(id=51, name='Pov (3D Generate)', public_name='Pov', type=0, sd_model_id=6,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
        Action(id=52, name='Pov (Art Generate)', public_name='Pov', type=0, sd_model_id=7,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
        Action(id=53, name='Pov (Semi realism Generate)', public_name='Pov', type=0, sd_model_id=8,
               lora_name='<lora:PovReverseCowgirlAnalv2:0.9>', raw_prompt1=''),
    ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0007_add_new_sd_model'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
