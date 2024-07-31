import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class ResultViewBottomButtons extends StatelessWidget {
  final MediaModel? model;
  const ResultViewBottomButtons({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return SizedBox(
      height: 60.h,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            flex: 4,
            child: FilledButton.icon(
              onPressed: () {},
              label: Text(
                model != null ? t.common.copy : t.generateView.repeat,
                style: textTheme.titleLarge!.copyWith(
                    color: colorScheme.onSecondary,
                    fontSize: 12.sp,
                    fontWeight: FontWeight.bold),
              ),
              icon: model != null
                  ? const SizedBox.shrink()
                  : SvgPicture.asset(Assets.icons.repeat),
              style: ButtonStyle(
                  backgroundColor:
                      WidgetStatePropertyAll(colorScheme.secondary)),
            ),
          ),
          const Gap(AppValues.kPadding / 2),
          Expanded(
              child: _MiniButton(
                  icon: SvgPicture.asset(
                    Assets.icons.download,
                    color: colorScheme.onPrimary,
                  ),
                  onTap: () {})),
          const Gap(AppValues.kPadding / 2),
          Expanded(
              child: _MiniButton(
                  icon: SvgPicture.asset(Assets.icons.share), onTap: () {})),
        ],
      ),
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
        visualDensity: VisualDensity.comfortable,
        color: AppColors.kSecondaryAdditionallyColor,
        shape: ContinuousRectangleBorder(
          borderRadius: BorderRadius.circular(AppValues.kRadius),
        ),
        padding: const EdgeInsets.all(AppValues.kPadding),
        child: icon);
  }
}
