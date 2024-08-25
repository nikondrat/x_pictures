def remove_file_from_s3(sender, instance, using, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


def job_remove_file_from_s3(sender, instance, using, **kwargs):
    if hasattr(instance, 'image'):
        instance.image.delete(save=False)
    if hasattr(instance, 'blur_image'):
        instance.blur_image.delete(save=False)
    if hasattr(instance, 'without_watermark_image'):
        instance.without_watermark_image.delete(save=False)
    if hasattr(instance, 'video'):
        instance.video.delete(save=False)
    if hasattr(instance, 'without_watermark_video'):
        instance.without_watermark.delete(save=False)
    if hasattr(instance, 'preview'):
        instance.preview.delete(save=False)
