import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/constant.dart';

class GradientButton extends StatelessWidget {
  final Function() onPressed;
  final String text;
  final bool isEnabled;
  final EdgeInsets? padding;
  final TextStyle? textStyle;

  const GradientButton({
    super.key,
    required this.onPressed,
    required this.text,
    this.isEnabled = true,
    this.padding,
    this.textStyle,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return GestureDetector(
      onTap: isEnabled ? onPressed : null,
      child: Container(
        height: 50.h,
        padding: padding ?? const EdgeInsets.all(AppValues.kPadding),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: isEnabled
                ? [colorScheme.primary, AppColors.kPrimaryAdditionallyColor]
                : [
                    colorScheme.primary.withOpacity(0.5),
                    AppColors.kPrimaryAdditionallyColor.withOpacity(0.5)
                  ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
          borderRadius: BorderRadius.circular(AppValues.kRadius),
        ),
        child: Center(
          child: AutoSizeText(
            text,
            style: textStyle ??
                textTheme.titleMedium!.copyWith(
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.5,
                  color: isEnabled
                      ? textTheme.titleMedium!.color
                      : textTheme.titleMedium!.color!.withOpacity(0.5),
                ),
          ),
        ),
      ),
    );
  }
}
