import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class InputWithTitleWidget extends StatelessWidget {
  final String title;
  final Widget inputWidget;

  const InputWithTitleWidget(
      {super.key, required this.title, required this.inputWidget});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: textTheme.titleMedium!.copyWith(color: colorScheme.outline),
        ),
        const Gap(AppValues.kPadding / 3),
        inputWidget,
        const Gap(AppValues.kPadding)
      ],
    );
  }
}
