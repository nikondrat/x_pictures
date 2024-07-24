import 'dart:io';

import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class CustomBackButton extends StatelessWidget {
  final Function()? onTap;
  const CustomBackButton({super.key, this.onTap});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;

    return IconButton(
      onPressed: () {
        if (onTap != null) {
          onTap!();
        } else {
          context.pop();
        }
      },
      icon: Icon(Platform.isAndroid ? Icons.arrow_back : Icons.arrow_back_ios,
          size: 18, color: colorScheme.outline),
    );
  }
}
