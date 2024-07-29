import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class CustomTabWidget extends StatelessWidget {
  final String title;
  final TextStyle? titleStyle;
  final bool isSelected;
  final Function() onTap;
  const CustomTabWidget({
    super.key,
    required this.title,
    this.titleStyle,
    this.isSelected = false,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return isSelected
        ? GradientButton(
            textStyle: textTheme.bodyLarge,
            padding:
                const EdgeInsets.symmetric(vertical: AppValues.kPadding / 4),
            onPressed: onTap,
            text: title)
        : GestureDetector(
            onTap: onTap,
            child: Text(
              title,
              style: textTheme.bodyLarge,
              textAlign: TextAlign.center,
            ),
          );
  }
}
