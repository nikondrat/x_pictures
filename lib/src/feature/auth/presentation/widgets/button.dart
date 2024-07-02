import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class AuthButton extends StatelessWidget {
  final String title;
  final Widget icon;
  final void Function() onPressed;
  final double windowHeight;

  const AuthButton({
    super.key,
    required this.icon,
    required this.title,
    required this.onPressed,
    required this.windowHeight,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return FilledButton.icon(
      onPressed: onPressed,
      icon: icon,
      label: AutoSizeText(
        title,
        style: textTheme.bodyLarge!.copyWith(
            color: AppColors.kBackgroundColor, fontWeight: FontWeight.bold),
        maxLines: 1,
      ),
      style: ButtonStyle(
          padding: WidgetStatePropertyAll(EdgeInsets.symmetric(
              vertical: windowHeight * .02, horizontal: AppValues.kPadding)),
          backgroundColor:
              const WidgetStatePropertyAll(AppColors.kSecondaryColor)),
    );
  }
}
