// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'package:flutter/material.dart';

class CustomAllText extends StatelessWidget {
  final void Function() onTap;
  const CustomAllText({
    super.key,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Text('All',
          style: TextStyle(
            fontWeight: FontWeight.w400,
            color: Colors.orange[800],
          )),
    );
  }
}
