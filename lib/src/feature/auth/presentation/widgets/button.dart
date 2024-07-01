import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class AuthButton extends StatelessWidget {
  final String title;
  final Widget icon;
  final void Function() onPressed;

  const AuthButton({
    super.key,
    required this.icon,
    required this.title,
    required this.onPressed,
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
        style: textTheme.headlineSmall!.copyWith(
            color: AppColors.kBackgroundColor, fontWeight: FontWeight.bold),
        maxLines: 1,
      ),
      style: const ButtonStyle(
          padding: WidgetStatePropertyAll(EdgeInsets.symmetric(
              vertical: AppValues.kPadding * 1.4,
              horizontal: AppValues.kPadding)),
          backgroundColor: WidgetStatePropertyAll(AppColors.kSecondaryColor)),
    );
  }
}
