import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/data.dart';

class CustomFloatingButton extends StatelessWidget {
  final String buttonName;
  final void Function() onTap;
  const CustomFloatingButton(
      {super.key, required this.buttonName, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 50.h,
      padding: EdgeInsets.only(
        left: 30.w,
      ),
      child: CustomButton(
        text: buttonName,
        onTap: onTap,
      ),
    );
  }
}
