import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class BackgroundSection extends StatelessWidget {
  final String title;
  final List<PackModel> packs;
  final Function(PackModel model) onTap;
  const BackgroundSection(
      {super.key,
      required this.title,
      required this.packs,
      required this.onTap});

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
              title,
              style: textTheme.titleLarge,
            ),
            TextButton(
                onPressed: () {
                  router.goNamed(AppViews.allStyles, extra: {
                    'title': title,
                    'items': packs,
                    'onTap': (PackModel model) {
                      onTap(model);
                    }
                  });
                },
                child: Text(t.common.all)),
          ],
        ),
        const Gap(AppValues.kPadding),
        SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: packs
                  .map((e) => BackgroundItem(
                      model: e,
                      //  cardHeight: section.cardHeight,
                      onTap: onTap))
                  .toList(),
            ))
      ],
    );
  }
}
