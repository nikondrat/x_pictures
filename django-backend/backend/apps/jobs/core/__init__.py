from .undress import Service as UndressService
from .undress import ServiceV2 as UndressWithoutMaskService
from .generate import ProxyService as GenerateService
from .generate import WhiteGenerate as WhiteGenerateService
from .instagram_undress import Service as InstagramUndressService
from .video import Service as VideoService

__all__ = (
    # Undress
    'UndressService',
    'UndressWithoutMaskService',
    # Generate
    'GenerateService',
    'WhiteGenerateService',
    # Instagram
    'InstagramUndressService',
    # Video
    'VideoService',
)
