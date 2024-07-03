import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class GenerateTags extends StatelessWidget {
  const GenerateTags({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    final List tags = [
      t.generateView.tags.fisheye,
      t.generateView.tags.oldAnime,
      t.generateView.tags.popArt,
      t.generateView.tags.darkLighting,
      '+ ...'
    ];

    return TitleWithBody(
      title: t.generateView.tags.title,
      action: const ResetButton(),
      child: Wrap(
        spacing: AppValues.kPadding / 2,
        runSpacing: AppValues.kPadding / 2,
        children: tags
            .map((e) => ActionChip(
                  onPressed: () {},
                  label: Text(e, style: textTheme.bodyLarge),
                  side: const BorderSide(color: AppColors.kOutlineColor),
                ))
            .toList(),
      ),
    );
  }
}
