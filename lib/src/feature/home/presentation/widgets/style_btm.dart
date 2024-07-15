import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class StyleBottomWidget extends StatelessWidget {
  final PackModel model;
  const StyleBottomWidget({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    // return ImageWithShader(url: model.url);

    return ClipRRect(
      borderRadius: BorderRadius.circular(AppValues.kRadius * 2),
      child: Stack(
        fit: StackFit.expand,
        children: [
          model.images.isNotEmpty
              ? ImageWithShader(url: model.images[0].url)
              : const Icon(Icons.hourglass_empty),
          Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              AutoSizeText(model.title, style: textTheme.headlineLarge),
              const Gap(AppValues.kPadding / 2),
              AutoSizeText('${model.length} ${t.profile.photos}',
                  style: textTheme.bodyLarge!
                      .copyWith(color: AppColors.kOutlineColor)),
              const Gap(AppValues.kPadding * 3)
            ],
          ),
          // Positioned(
          //   bottom: 40,
          //   // left: MediaQuery.of(context).size.width / 2.w - 20.w,
          //   child: Text('Office'),
          // ),
          // Positioned(
          //   bottom: 30,
          //   // left: MediaQuery.of(context).size.width / 2.w - 15.w,
          //   child: Text(
          //     '6 photos',
          //     style: TextStyle(
          //       fontWeight: FontWeight.w400,
          //       color: const Color(0xff7C7C9B),
          //     ),
          //   ),
          // ),
        ],
      ),
    );
  }
}
