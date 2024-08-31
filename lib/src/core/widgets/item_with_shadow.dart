import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class ItemWithShadow extends StatelessWidget {
  final PackModel model;
  const ItemWithShadow({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Stack(
      fit: StackFit.expand,
      children: [
        ShaderMask(
            blendMode: BlendMode.srcATop,
            shaderCallback: (Rect bounds) {
              return const LinearGradient(
                colors: [Colors.black, Colors.transparent],
                begin: Alignment.bottomCenter,
                end: Alignment.topCenter,
              ).createShader(bounds);
            },
            child: model.images.isNotEmpty
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(AppValues.kRadius),
                    child: CachedNetworkImage(
                      imageUrl: model.images[0].url,
                      fit: BoxFit.cover,
                      errorWidget: (context, url, error) {
                        return Center(
                          child: Text('$error'),
                        );
                      },
                    ),
                  )
                : DecoratedBox(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(AppValues.kRadius),
                      color: AppColors.kSecondaryAdditionallyColor,
                    ),
                    child: const Center(
                      child: Icon(Icons.image_not_supported_outlined),
                    ),
                  )),
        Align(
            alignment: Alignment.bottomLeft,
            child: Padding(
              padding: const EdgeInsets.symmetric(
                  horizontal: AppValues.kPadding, vertical: AppValues.kPadding),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.end,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  AutoSizeText(
                    model.title,
                    style: textTheme.titleMedium!
                        .copyWith(color: colorScheme.onSurface),
                  ),
                  if (model.images.isNotEmpty)
                    AutoSizeText('${model.length} ${t.profile.photos}',
                        style: textTheme.titleSmall!
                            .copyWith(color: AppColors.kOutlineColor)),
                ],
              ),
            )),
      ],
    );
  }
}
