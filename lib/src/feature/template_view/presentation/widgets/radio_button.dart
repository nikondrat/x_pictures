import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class RadioButton extends StatelessWidget {
  final String text;
  final bool isSelected;
  final dynamic value;
  final dynamic groupValue;
  final double? price;
  final String? subtitle;
  final bool showDiscount;
  final void Function(dynamic) onChanged;

  const RadioButton(
      {super.key,
      this.showDiscount = false,
      required this.text,
      required this.isSelected,
      required this.value,
      this.price,
      this.subtitle,
      required this.groupValue,
      required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme scheme = themeData.colorScheme;

    return GestureDetector(
      onTap: () {
        onChanged(value);
      },
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          Container(
            margin: const EdgeInsets.only(bottom: AppValues.kPadding),
            padding: EdgeInsets.symmetric(vertical: AppValues.kPadding / 4),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(AppValues.kRadius),
              border: Border.all(
                color: isSelected ? scheme.primary : AppColors.kOutlineColor,
              ),
            ),
            child: Row(
              children: [
                Radio(
                  value: value,
                  groupValue: groupValue,
                  onChanged: onChanged,
                ),
                Expanded(
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            AutoSizeText(
                              text,
                              style: AppStyles.title2TextStyle.copyWith(
                                  color: Colors.white, fontSize: 14.sp),
                            ),
                            if (subtitle != null)
                              AutoSizeText(
                                subtitle!,
                                style: textTheme.bodyMedium!.copyWith(
                                    color: AppColors.kOutlineColor,
                                    fontSize: 12.sp),
                              )
                          ],
                        ),
                      ),
                      if (price != null)
                        AutoSizeText('€$price/${t.template.week}',
                            style: textTheme.bodyLarge!.copyWith(
                                fontWeight: FontWeight.bold, fontSize: 14.sp)),
                      const Gap(AppValues.kPadding)
                    ],
                  ),
                ),
              ],
            ),
          ),
          if (showDiscount)
            Positioned(
              right: 20,
              top: -15,
              child: Container(
                // margin: EdgeInsets.only(right: 20.r, bottom: 10.r),
                decoration: BoxDecoration(
                    color: scheme.onPrimary,
                    borderRadius: BorderRadius.circular(AppValues.kRadius.r)),
                padding: EdgeInsets.all(6.r),
                child: AutoSizeText(
                  "${t.template.save} 90%",
                  style:
                      textTheme.bodySmall!.copyWith(color: scheme.onSecondary),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
