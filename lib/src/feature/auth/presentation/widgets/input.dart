import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';

class InputWithTitleWidget extends StatelessWidget {
  final String title;
  final Widget inputWidget;

  const InputWithTitleWidget(
      {super.key, required this.title, required this.inputWidget});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        AutoSizeText(
          title,
          maxFontSize: 22,
          maxLines: 1,
          style: textTheme.titleMedium!
              .copyWith(color: colorScheme.outline, fontSize: 12.sp),
        ),
        Gap(6.h),
        inputWidget,
        Gap(12.h),
      ],
    );
  }
}
