import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class MediaItem extends StatelessWidget {
  final MediaModel model;
  const MediaItem({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData theme = Theme.of(context);
    final ColorScheme colorScheme = theme.colorScheme;

    final MediaBodyStore? store = context.read();

    return GestureDetector(
      onTap: () {
        if (store != null && store.isSelect) {
          model.toggleSelected();
        } else {
          if (model.type == MediaType.video) {
            router.goNamed(AppViews.resultView, extra: {'model': model});
          } else {
            showDialog(
                context: context,
                barrierDismissible: true,
                builder: (_) {
                  return PopupImage(
                    url: model.url,
                    isProfile: true,
                  );
                });
          }
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
                  size: 16,
                ),
              ),
            ),
          ),
          Observer(builder: (_) {
            return model.isSelected
                ? Align(
                    alignment: Alignment.bottomRight,
                    child: Container(
                        margin: const EdgeInsets.all(AppValues.kPadding / 2),
                        padding: const EdgeInsets.all(AppValues.kPadding / 4),
                        decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: colorScheme.primary.withOpacity(.4)),
                        child: const Icon(
                          Icons.done,
                          size: 12,
                        )))
                : const SizedBox.shrink();
          })
        ],
      ),
    );
  }
}
