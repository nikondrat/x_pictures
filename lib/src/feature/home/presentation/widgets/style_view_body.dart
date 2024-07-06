import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class StyleViewBody extends StatelessWidget {
  final StyleModel model;
  const StyleViewBody({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    final bool hasImages = model.images != null && model.images!.isNotEmpty;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        AutoSizeText(t.homeView.what_style, style: textTheme.headlineSmall),
        const Gap(AppValues.kPadding / 2),
        AutoSizeText(
          model.description,
          style: textTheme.titleLarge!.copyWith(color: AppColors.kOutlineColor),
        ),
        const Gap(AppValues.kPadding / 2),
        AutoSizeText(t.homeView.for_what, style: textTheme.headlineSmall),
        const Gap(AppValues.kPadding / 2),
        Column(
          children: model.data.map((e) {
            return AutoSizeText(
              '   •  $e',
              style: textTheme.titleLarge!
                  .copyWith(color: AppColors.kOutlineColor),
            );
          }).toList(),
        ),
        if (hasImages)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: AppValues.kPadding),
            child: AutoSizeText(t.homeView.outputs,
                style: textTheme.headlineSmall),
          ),
        if (hasImages)
          GridView(
              shrinkWrap: true,
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                  crossAxisSpacing: AppValues.kPadding,
                  mainAxisSpacing: AppValues.kPadding,
                  childAspectRatio: .7,
                  maxCrossAxisExtent: 320),
              children: model.images!.map((e) {
                return ClipRRect(
                  borderRadius: BorderRadius.circular(AppValues.kRadius),
                  child: CachedNetworkImage(
                    imageUrl: e,
                    fit: BoxFit.cover,
                  ),
                );
              }).toList())
      ],
    );
  }
}
