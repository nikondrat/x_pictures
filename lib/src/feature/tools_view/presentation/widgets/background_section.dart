import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class BackgroundSection extends StatelessWidget {
  final BackgroundSectionModel section;
  const BackgroundSection({super.key, required this.section});

  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    void onTap(ItemModel model) {
      router.goNamed(AppViews.imageWithBackground, extra: {'model': model});
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            AutoSizeText(
              section.title,
              style: textTheme.titleLarge,
            ),
            Padding(
              padding: const EdgeInsets.only(right: AppValues.kPadding),
              child: TextButton(
                  onPressed: () {
                    router.goNamed(AppViews.allStyles, extra: {
                      'title': t.backgrounds.title,
                      'items': section.items,
                      'onTap': (ItemModel model) {
                        onTap(model);
                      }
                    });
                  },
                  child: Text(t.common.all)),
            ),
          ],
        ),
        Gap(AppValues.kPadding),
        SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: section.items
                  .map((e) => BackgroundItem(model: e, onTap: onTap))
                  .toList(),
            ))
      ],
    );
  }
}
