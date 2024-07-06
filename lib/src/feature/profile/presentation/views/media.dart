import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class MediaView extends StatelessWidget {
  final Function() onBannerTap;
  final List<MediaModel> urls;

  const MediaView({
    super.key,
    required this.onBannerTap,
    required this.urls,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (urls.isNotEmpty) const Gap(AppValues.kPadding),
        urls.isEmpty
            ? IntrinsicHeight(
                child: GestureDetector(
                  onTap: onBannerTap,
                  child: Image.asset(
                    Assets.images.banner2.path,
                    fit: BoxFit.contain,
                  ),
                ),
              )
            : Expanded(
                child: GridView.builder(
                    gridDelegate:
                        const SliverGridDelegateWithMaxCrossAxisExtent(
                            crossAxisSpacing: AppValues.kPadding,
                            childAspectRatio: 0.6,
                            mainAxisSpacing: AppValues.kPadding,
                            maxCrossAxisExtent: 200),
                    itemBuilder: (context, index) =>
                        MediaItem(model: urls[index]),
                    itemCount: urls.length),
              ),
      ],
    );
  }
}
