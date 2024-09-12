import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class GenerateTags extends StatelessWidget {
  const GenerateTags({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    final GenerateStore store = context.read<GenerateStore>();

    // final List tags = [
    //   t.generateView.tags.fisheye,
    //   t.generateView.tags.oldAnime,
    //   t.generateView.tags.popArt,
    //   t.generateView.tags.darkLighting,
    //   '+ ...'
    // ];

    return TitleWithBody(
      title: t.generateView.tags.title,
      action: ResetButton(
        onPressed: () {
          store.markAllTagsAsNotSelected();
        },
      ),
      padding: AppValues.kPadding / 2,
      child: IntrinsicHeight(child: Observer(builder: (_) {
        return Wrap(
            spacing: 6,
            children: store.tags
                .map((e) => ActionChip(
                      onPressed: () => e.setIsSelected(!e.isSelected),
                      backgroundColor: AppColors.kSecondaryAdditionallyColor,
                      label: Text(e.title,
                          maxLines: 2, style: textTheme.bodyMedium),
                      side: BorderSide(
                          color: e.isSelected
                              ? AppColors.kPrimaryColor
                              : AppColors.kOutlineColor),
                    ))
                .toList());
      })),
    );
  }
}
