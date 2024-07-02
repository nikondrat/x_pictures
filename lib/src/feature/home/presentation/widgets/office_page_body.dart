import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';

class OfficePageBody extends StatelessWidget {
  const OfficePageBody({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 15.w),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            height: 10.h,
          ),
          Text(
            'What\'s the style?',
            style: AppStyles.title2TextStyle,
          ),
          SizedBox(
            height: 10.h,
          ),
          Text(
            'This style is suitable for showing in a business style to show all your inner qualities',
            style: AppStyles.subTitleTextStyle,
          ),
          SizedBox(
            height: 10.h,
          ),
          Text(
            'For what?',
            style: AppStyles.title2TextStyle,
          ),
          SizedBox(
            height: 10.h,
          ),
          Text.rich(
            TextSpan(
              children: [
                TextSpan(
                  text: '. Description',
                  style: AppStyles.subTitleTextStyle,
                ),
                TextSpan(
                  text: '\n. Description',
                  style: AppStyles.subTitleTextStyle,
                ),
                TextSpan(
                  text: '\n. Description',
                  style: AppStyles.subTitleTextStyle,
                ),
              ],
            ),
          ),
          SizedBox(
            height: 10.h,
          ),
          Text(
            'Example outputs',
            style: AppStyles.title2TextStyle,
          ),
          SizedBox(
            height: 10.h,
          ),
        ],
      ),
    );
  }
}
