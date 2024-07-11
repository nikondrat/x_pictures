import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class MediaView extends StatelessWidget {
  final Function() onBannerTap;
  final List<MediaModel> items;

  const MediaView({
    super.key,
    required this.onBannerTap,
    required this.items,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Gap(AppValues.kPadding),
        Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
          FilledButton(
              style: const ButtonStyle(
                  backgroundColor: WidgetStatePropertyAll(
                      AppColors.kSecondaryAdditionallyColor)),
              onPressed: () {},
              child: AutoSizeText(t.common.select_all)),
          FilledButton(
              style: const ButtonStyle(
                  backgroundColor: WidgetStatePropertyAll(
                      AppColors.kSecondaryAdditionallyColor)),
              onPressed: () {},
              child: AutoSizeText(t.common.select)),
        ]),
        if (items.isNotEmpty) const Gap(AppValues.kPadding),
        items.isEmpty
            ? IntrinsicHeight(
                child: GestureDetector(
                  onTap: onBannerTap,
                  child: Image.asset(
                    Assets.images.banner2.path,
                    fit: BoxFit.contain,
                  ),
                ),
              )
            : Flexible(
                child: MediaBody(
                  items: items,
                ),
              )
        // Expanded(
        //     child: GridView.builder(
        //         gridDelegate:
        //             const SliverGridDelegateWithMaxCrossAxisExtent(
        //                 crossAxisSpacing: AppValues.kPadding,
        //                 childAspectRatio: 0.6,
        //                 mainAxisSpacing: AppValues.kPadding,
        //                 maxCrossAxisExtent: 200),
        //         itemBuilder: (context, index) =>
        //             MediaItem(model: urls[index]),
        //         itemCount: urls.length),
        //   ),
      ],
    );
  }
}
