import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class RadioButton extends StatelessWidget {
  final String text;
  final bool isSelected;
  final dynamic value;
  final dynamic groupValue;
  final void Function(dynamic) onChanged;

  const RadioButton(
      {super.key,
      required this.text,
      required this.isSelected,
      required this.value,
      required this.groupValue,
      required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return RadioListTile(
        contentPadding: const EdgeInsets.symmetric(
            horizontal: AppValues.kPadding * 0.8,
            vertical: AppValues.kPadding * 0.25),
        shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppValues.kRadius),
            side: BorderSide(
              color: isSelected ? Colors.orange[900]! : const Color(0xff3B3B5A),
              // width: 2
            )),
        activeColor: Colors.orange[900],
        // fillColor: WidgetStateProperty.all(const Color(0xff3B3B5A)),

        title: Text(
          text,
          style: AppStyles.title2TextStyle
              .copyWith(color: Colors.white, fontSize: 10.sp),
        ),
        value: value,
        groupValue: groupValue,
        onChanged: onChanged);
  }
}
