import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class BackgroundSection extends StatelessWidget {
  final BackgroundSectionModel section;
  final Function(ItemModel model) onTap;
  const BackgroundSection(
      {super.key, required this.section, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        const Gap(AppValues.kPadding),
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
        const Gap(AppValues.kPadding),
        SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: section.items
                  .map((e) => BackgroundItem(
                      model: e, cardHeight: section.cardHeight, onTap: onTap))
                  .toList(),
            ))
      ],
    );
  }
}
