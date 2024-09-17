import 'dart:ui';

import 'package:flutter/widgets.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/data.dart';

class BottomBarDecoration extends StatelessWidget {
  final Widget child;
  const BottomBarDecoration({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20.r)),
        child: BackdropFilter(
            filter: ImageFilter.blur(
                sigmaX: 5.0, sigmaY: 5.0), // Значения размытости
            child: DecoratedBox(
                // decoration: BoxDecoration(),
                decoration: BoxDecoration(
                  border: const Border(
                      top: BorderSide(
                    color: Color(0xFF3B3B5A),
                  )),
                  borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(20.r),
                    topRight: Radius.circular(20.r),
                  ),
                  color:
                      //  const Color(0xff0D1120).withAlpha(245)
                      AppColors.kSecondaryAdditionallyColor.withOpacity(0.85),
                ),
                child: Padding(
                    padding: const EdgeInsets.only(bottom: 14),
                    child: child))));
  }
}
