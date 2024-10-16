import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
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
            minFontSize: 17,
            maxFontSize: 40,
            style: titleStyle ??
                textTheme.headlineMedium!.copyWith(fontSize: 30.sp),
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
                maxFontSize: 28,
                textAlign: TextAlign.center,
                style: descriptionStyle ??
                    textTheme.titleLarge!.copyWith(
                        color: AppColors.kOutlineColor, fontSize: 17.sp),
                maxLines: 2,
              ),
            )),
      ],
    );
  }
}
