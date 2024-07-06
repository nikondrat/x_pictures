import 'package:flutter/material.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class RadioButton extends StatelessWidget {
  final String text;
  final bool isSelected;
  final dynamic value;
  final dynamic groupValue;
  final void Function(dynamic) onChanged;

  const RadioButton({
    super.key,
    required this.text,
    required this.isSelected,
    required this.value,
    required this.groupValue,
    required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return RadioListTile(
        shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppValues.kRadius),
            side: BorderSide(color: isSelected ? Colors.orange[900]! : const Color(0xff6F6F72))
        ),
        title: Text(text,
          style: AppStyles.buttonTextStyle.copyWith(
              color: Colors.white
          ),),
        value: value,
        groupValue: groupValue,
        onChanged: onChanged);
  }
}
