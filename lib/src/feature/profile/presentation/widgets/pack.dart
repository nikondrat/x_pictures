import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_slidable/flutter_slidable.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class PackItem extends StatelessWidget {
  final PackModel pack;
  const PackItem({super.key, required this.pack});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;
    final TextTheme textTheme = themeData.textTheme;

    return Slidable(
      endActionPane: ActionPane(motion: const ScrollMotion(), children: [
        SlidableAction(
          onPressed: (_) {},
          backgroundColor: colorScheme.error,
          borderRadius: const BorderRadius.horizontal(
              right: Radius.circular(AppValues.kRadius)),
          label: t.settings.delete.title,
        ),
      ]),
      child: GestureDetector(
        onTap: () {
          router.pushNamed(AppViews.photosView, extra: {'urls': pack.urls});
        },
        child: Container(
            margin: const EdgeInsets.only(bottom: AppValues.kPadding),
            decoration: BoxDecoration(
              color: AppColors.kSecondaryAdditionallyColor,
              borderRadius: BorderRadius.circular(AppValues.kRadius),
            ),
            padding: const EdgeInsets.all(AppValues.kPadding),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                AutoSizeText(pack.title, style: textTheme.titleLarge),
                const Gap(AppValues.kPadding / 3),
                AutoSizeText(
                  pack.progress != null
                      ? '${t.profile.getting_ready} ~${pack.progress} ${t.profile.minutes}'
                      : '${pack.length} ${t.profile.photos}',
                  style: textTheme.bodyLarge!
                      .copyWith(color: AppColors.kOutlineColor),
                ),
                const Gap(AppValues.kPadding / 3),
                LayoutBuilder(
                  builder: (BuildContext context, BoxConstraints constraints) {
                    return Row(
                      children: pack.urls
                          .map((url) => Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.all(
                                      AppValues.kPadding / 4),
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(
                                        AppValues.kRadius / 2),
                                    child: CachedNetworkImage(
                                      imageUrl: url,
                                      fit: BoxFit.cover,
                                      width: constraints.maxWidth /
                                          pack.urls.length,
                                      height: constraints.maxWidth /
                                          pack.urls.length,
                                    ),
                                  ),
                                ),
                              ))
                          .toList(),
                    );
                  },
                )
              ],
            )),
      ),
    );
  }
}
