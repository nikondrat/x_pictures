import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class DisclaimarPage extends StatelessWidget {
  const DisclaimarPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(textName: 'Disclaimer'),
      floatingActionButton: CustomFloatingButton(
        buttonName: 'Get started',
        onTap: () {
          router.goNamed(AppViews.instructionPageRoute);
        },
      ),
      body: Padding(
        padding: EdgeInsets.only(left: 15.w, right: 15.w),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(10.r),
              ),
              child: Image.asset(
                AppImages.testImage,
                fit: BoxFit.cover,
              ),
            ),
            SizedBox(
              height: 20.h,
            ),
            Text(
              'How it works?',
              style: AppStyles.title2TextStyle,
            ),
            SizedBox(
              height: 10.h,
            ),
            Text(
              'Описание правил',
              style: AppStyles.subTitleTextStyle,
            ),
          ],
        ),
      ),
    );
  }
}
