import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class MediaItem extends StatelessWidget {
  final MediaModel model;
  const MediaItem({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData theme = Theme.of(context);
    final ColorScheme colorScheme = theme.colorScheme;

    return GestureDetector(
      onTap: () {
        if (model.type == MediaType.video) {
          router.goNamed(AppViews.resultView, extra: {'model': model});
        } else {
          showDialog(
              context: context,
              barrierDismissible: true,
              builder: (_) {
                return PopupImage(url: model.url, isProfile: true,);
              });
          // router.goNamed(AppViews.image);
        }
      },
      child: Stack(
        fit: StackFit.expand,
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(AppValues.kRadius),
            child: CachedNetworkImage(
              imageUrl: model.url,
              fit: BoxFit.cover,
            ),
          ),
          Align(
            alignment: Alignment.topRight,
            child: GestureDetector(
              onTap: () {},
              child: Container(
                margin: const EdgeInsets.all(AppValues.kPadding / 2),
                padding: const EdgeInsets.all(AppValues.kPadding / 4),
                decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.grey.shade900.withAlpha(160)),
                child: Icon(
                  Icons.file_download_outlined,
                  color: colorScheme.onSurface,
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}
