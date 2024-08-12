import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
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

    return Stack(
      children: [
        RadioListTile(
            visualDensity: VisualDensity.comfortable,
            dense: true,
            contentPadding: const EdgeInsets.symmetric(
                horizontal: AppValues.kPadding * 0.8,
                vertical: AppValues.kPadding * 0.25),
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(AppValues.kRadius),
                side: BorderSide(
                  color: isSelected
                      ? Colors.orange[900]!
                      : const Color(0xff3B3B5A),
                )),
            activeColor: Colors.orange[900],
            title: Row(
              children: [
                Expanded(
                  child: AutoSizeText(
                    text,
                    style: AppStyles.title2TextStyle
                        .copyWith(color: Colors.white, fontSize: 14.sp),
                  ),
                ),
                if (price != null)
                  Padding(
                    padding: EdgeInsets.only(top: showDiscount ? 14.r : 0),
                    child: AutoSizeText('€$price/${t.template.week}',
                        style: textTheme.bodyLarge!.copyWith(
                            fontWeight: FontWeight.bold, fontSize: 14.sp)),
                  ),
              ],
            ),
            subtitle: subtitle != null
                ? AutoSizeText(
                    subtitle!,
                    style: textTheme.bodyMedium!.copyWith(
                        color: AppColors.kOutlineColor, fontSize: 12.sp),
                  )
                : null,
            value: value,
            groupValue: groupValue,
            onChanged: onChanged),
        if (showDiscount)
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Container(
                margin: EdgeInsets.only(right: 20.r, bottom: 10.r),
                decoration: BoxDecoration(
                    color: scheme.onPrimary,
                    borderRadius: BorderRadius.circular(AppValues.kRadius.r)),
                padding: EdgeInsets.all(6.r),
                child: Center(
                  child: AutoSizeText(
                    "${t.template.save} 90%",
                    style: textTheme.bodySmall!
                        .copyWith(color: scheme.onSecondary),
                  ),
                ),
              ),
            ],
          ),
      ],
    );
  }
}
