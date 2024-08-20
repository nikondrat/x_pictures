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
      action: const ResetButton(),
      child: Observer(
          builder: (context) => Wrap(
              spacing: AppValues.kPadding / 4,
              runSpacing: AppValues.kPadding / 4,
              children: store.tags
                  .map((e) => ActionChip(
                        onPressed: () {},
                        backgroundColor: AppColors.kSecondaryAdditionallyColor,
                        label: Text(e.title, style: textTheme.bodyLarge),
                        side: const BorderSide(color: AppColors.kOutlineColor),
                      ))
                  .toList())),
      // Wrap(
      //       spacing: AppValues.kPadding / 2,
      //       runSpacing: AppValues.kPadding / 2,
      //       children: store.tags
      //           .map((e) => ActionChip(
      //                 onPressed: () {},
      //                 backgroundColor:
      //                     AppColors.kSecondaryAdditionallyColor,
      //                 label:
      //                     AutoSizeText(e.title, style: textTheme.bodyLarge),
      //                 side:
      //                     const BorderSide(color: AppColors.kOutlineColor),
      //               ))
      //           .toList(),
      //     )),
    );
  }
}
