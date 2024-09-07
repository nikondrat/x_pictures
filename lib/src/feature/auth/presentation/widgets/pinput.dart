import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:go_router/go_router.dart';
import 'package:pinput/pinput.dart';
import 'package:x_pictures/src/data.dart';

class CustomPinput extends StatelessWidget {
  final double windowHeight;
  final double windowWidth;
  const CustomPinput(
      {super.key, required this.windowHeight, required this.windowWidth});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    final double width = windowWidth * .8;
    final double height = windowHeight * .11.spMin;

    return Pinput(
      length: 5,
      errorText: t.auth.errors.invalid_code,
      errorTextStyle: textTheme.bodyLarge!.copyWith(
        color: colorScheme.error,
      ),
      // AppStyles.subTitleTextStyle.copyWith(
      //   color: const Color(0xffFF453A),
      // ),
      focusedPinTheme: PinTheme(
          height: height,
          width: width,
          decoration: BoxDecoration(
            // color: colorScheme.primary,
            border: Border.all(
              color: colorScheme.primary,
            ),
            borderRadius: BorderRadius.circular(AppValues.kRadius.r),
          ),
          textStyle:
              textTheme.displaySmall!.copyWith(color: colorScheme.onPrimary)
          // TextStyle(
          //   color: Colors.white,

          //   // fontSize: 19.sp,
          // ),
          ),
      defaultPinTheme: PinTheme(
          height: height,
          width: width,
          decoration: BoxDecoration(
            // color: AppColors.kPrimaryColor,
            border: Border.all(
              color: const Color(0xff3B3B5A),
            ),
            borderRadius: BorderRadius.circular(AppValues.kRadius.r),
          ),
          textStyle:
              textTheme.displaySmall!.copyWith(color: colorScheme.onPrimary)
          // textStyle: TextStyle(
          //   color: Colors.white,
          //   // fontSize: 19.sp,
          // ),
          ),
      onCompleted: (value) {
        if (value == '22222') {
          context.goNamed(AppViews.newPassword);
        }
      },
      onTapOutside: (event) => FocusScope.of(context).unfocus(),
      validator: (pin) {
        if (pin == '22222') return null;

        /// Text will be displayed under the Pinput
        return 'Pin is incorrect';
      },
    );
  }
}
