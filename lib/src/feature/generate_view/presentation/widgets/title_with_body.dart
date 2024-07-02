import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class TitleWithBody extends StatelessWidget {
  final String title;
  final Widget? action;
  final Widget child;
  const TitleWithBody(
      {super.key, required this.child, required this.title, this.action});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: textTheme.headlineSmall!.copyWith(
                  color: colorScheme.secondary, fontWeight: FontWeight.bold),
            ),
            if (action != null) action!,
          ],
        ),
        const Gap(AppValues.kPadding),
        child
      ],
    );
  }
}
