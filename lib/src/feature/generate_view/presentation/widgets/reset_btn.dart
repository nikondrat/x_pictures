import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class ResetButton extends StatelessWidget {
  final Function() onPressed;
  const ResetButton({
    super.key,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return TextButton(
        onPressed: onPressed,
        child: Text(
          t.common.reset,
          style: textTheme.bodyLarge!.copyWith(color: colorScheme.outline),
        ));
  }
}
