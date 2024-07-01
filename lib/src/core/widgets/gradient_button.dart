import 'package:flutter/material.dart';
import 'package:x_pictures/src/core/constant/constant.dart';

class GradientButton extends StatelessWidget {
  final Function() onPressed;
  final String text;

  const GradientButton(
      {super.key, required this.onPressed, required this.text});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return GestureDetector(
      onTap: onPressed,
      child: Container(
        padding: const EdgeInsets.all(AppValues.kPadding),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              colorScheme.primary,
              AppColors.kPrimaryAdditionallyColor,
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
          borderRadius: BorderRadius.circular(AppValues.kRadius),
        ),
        child: Center(
          child: Text(text,
              style: textTheme.headlineSmall!
                  .copyWith(fontWeight: FontWeight.bold)),
        ),
      ),
    );
  }
}
