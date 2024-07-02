import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class CustomBackButton extends StatelessWidget {
  const CustomBackButton({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;

    return IconButton(
      onPressed: () => context.pop(),
      icon: Icon(Icons.arrow_back_ios, size: 18, color: colorScheme.outline),
    );
  }
}
