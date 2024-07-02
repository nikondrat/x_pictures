import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class TitleWithDesc extends StatelessWidget {
  final String title;
  final TextStyle? titleStyle;
  final String description;
  final TextStyle? descriptionStyle;
  const TitleWithDesc(
      {super.key,
      required this.title,
      required this.description,
      this.titleStyle,
      this.descriptionStyle});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Column(
      children: [
        Align(
          alignment: Alignment.center,
          child: AutoSizeText(
            title,
            minFontSize: 16,
            style: titleStyle ??
                textTheme.displaySmall!.copyWith(fontWeight: FontWeight.bold),
            maxLines: 1,
          ),
        ),
        const Gap(AppValues.kPadding / 2),
        Align(
            alignment: Alignment.center,
            child: Padding(
              padding: const EdgeInsets.symmetric(
                  horizontal: AppValues.kPadding * 2),
              child: AutoSizeText(
                description,
                textAlign: TextAlign.center,
                style: descriptionStyle ??
                    textTheme.bodyLarge!
                        .copyWith(color: themeData.colorScheme.outline),
                maxLines: 2,
              ),
            )),
      ],
    );
  }
}
