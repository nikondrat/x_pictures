import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class DecoratedContentWidget extends StatelessWidget {
  final String content;
  const DecoratedContentWidget({super.key, required this.content});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Row(children: [
      Expanded(
          child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(AppValues.kRadius),
          color: AppColors.kSecondaryAdditionallyColor,
        ),
        padding: const EdgeInsets.all(AppValues.kPadding),
        child: AutoSizeText(
          content,
          style: textTheme.bodyMedium!.copyWith(color: colorScheme.outline),
        ),
      ))
    ]);
  }
}
