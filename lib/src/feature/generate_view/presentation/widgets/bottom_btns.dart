import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class ResultViewBottomButtons extends StatelessWidget {
  const ResultViewBottomButtons({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Row(
      children: [
        Expanded(
          flex: 5,
          child: FilledButton.icon(
            onPressed: () {},
            label: Text(
              t.generateView.repeat,
              style: textTheme.titleLarge!.copyWith(
                  color: colorScheme.onSecondary, fontWeight: FontWeight.bold),
            ),
            icon: SvgPicture.asset(Assets.icons.generate),
            style: ButtonStyle(
                padding: const WidgetStatePropertyAll(
                    EdgeInsets.all(AppValues.kPadding)),
                backgroundColor: WidgetStatePropertyAll(colorScheme.secondary)),
          ),
        ),
        const Gap(AppValues.kPadding / 2),
        Expanded(
            child: _MiniButton(
                icon: const Icon(Icons.file_download_outlined), onTap: () {})),
        const Gap(AppValues.kPadding / 2),
        Expanded(
            child: _MiniButton(
                icon: const Icon(Icons.ios_share_outlined), onTap: () {})),
      ],
    );
  }
}

class _MiniButton extends StatelessWidget {
  final Widget icon;
  final Function() onTap;
  const _MiniButton({required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return MaterialButton(
        onPressed: onTap,
        color: AppColors.kSecondaryAdditionallyColor,
        shape: ContinuousRectangleBorder(
          borderRadius: BorderRadius.circular(AppValues.kRadius),
        ),
        padding: const EdgeInsets.all(AppValues.kPadding),
        child: icon);
  }
}
