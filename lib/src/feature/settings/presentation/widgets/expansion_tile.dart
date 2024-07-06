import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class CustomExpansionTile extends StatelessWidget {
  final String title;
  final String content;
  const CustomExpansionTile(
      {super.key, required this.title, required this.content});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return ExpansionTile(
      title: Text(
        title,
        style: textTheme.titleLarge!.copyWith(fontWeight: FontWeight.w700),
      ),
      tilePadding: const EdgeInsets.symmetric(
          vertical: AppValues.kPadding / 2, horizontal: AppValues.kPadding),
      backgroundColor: AppColors.kSecondaryAdditionallyColor,
      collapsedBackgroundColor: AppColors.kSecondaryAdditionallyColor,
      collapsedShape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppValues.kRadius),
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppValues.kRadius),
      ),
      iconColor: AppColors.kOutlineColor,
      childrenPadding: const EdgeInsets.symmetric(
          horizontal: AppValues.kPadding, vertical: AppValues.kPadding / 2),
      children: [
        Row(
          children: [
            Expanded(
              child: AutoSizeText(
                content,
                style: textTheme.bodyLarge!
                    .copyWith(color: AppColors.kOutlineColor),
              ),
            ),
          ],
        )
      ],
    );
  }
}
