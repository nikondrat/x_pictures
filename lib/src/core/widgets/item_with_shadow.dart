import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class ItemWithShadow extends StatelessWidget {
  final ItemModel model;
  final Function(ItemModel model) onTap;
  const ItemWithShadow({super.key, required this.model, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return GestureDetector(
      onTap: () => onTap(model),
      child: Stack(
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
              child: ClipRRect(
                borderRadius: BorderRadius.circular(AppValues.kRadius),
                child: CachedNetworkImage(
                  imageUrl: model.url,
                  fit: BoxFit.cover,
                ),
              )),
          Align(
              alignment: Alignment.bottomLeft,
              child: Padding(
                padding: const EdgeInsets.symmetric(
                    horizontal: AppValues.kPadding,
                    vertical: AppValues.kPadding),
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
                    if (model.subTitle != null)
                      AutoSizeText(model.subTitle!,
                          style: textTheme.titleSmall!
                              .copyWith(color: AppColors.kOutlineColor)),
                  ],
                ),
              )),
        ],
      ),
    );
  }
}
