import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class HairStyleListItems extends StatelessWidget {
  const HairStyleListItems({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: EdgeInsets.only(left: 12.w, right: 20.w),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Hair style',
                style: AppStyles.head1TextStyle,
              ),
              CustomAllText(
                onTap: () {
                  router.goNamed(AppViews.viewAllPageRoute);
                },
              ),
            ],
          ),
        ),
        Padding(
          padding: EdgeInsets.only(left: 12.w, top: 10.h),
          child: SizedBox(
            height: 130.h,
            width: double.infinity,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              physics: const BouncingScrollPhysics(),
              itemCount: 10,
              itemBuilder: (BuildContext context, int index) {
                return Padding(
                  padding: EdgeInsets.only(right: 10.w),
                  child: const ImageItemHomePage(),
                );
              },
            ),
          ),
        ),
      ],
    );
  }
}
