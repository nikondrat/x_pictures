import 'package:flutter/material.dart';

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
    return ListTile(
      title: Text(text),
      leading: Radio(
          value: value,
          groupValue: groupValue,
          onChanged: onChanged),
    );
  }
}
