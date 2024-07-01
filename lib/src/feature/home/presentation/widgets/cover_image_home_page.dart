import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/core/constant/icons.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class CoverImageHomePage extends StatelessWidget {
  const CoverImageHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(20.r),
          bottomRight: Radius.circular(20.r),
        ),
      ),
      child: Stack(
        children: [
          CachedNetworkImage(
            imageUrl:
                'https://savilerowco.com/wp/wp-content/uploads/2017/02/11.jpg',
            height: 250.h,
            fit: BoxFit.cover,
          ),
          Positioned(
            top: 40.h,
            left: MediaQuery.of(context).size.width / 2 - 10.w,
            child: SvgPicture.asset(AppIcons.xIcon),
          ),
          Positioned(
            top: 40,
            right: 20,
            child: SvgPicture.asset(
              AppIcons.proIcon,
              width: 65.w,
            ),
          ),
          Positioned(
            left: MediaQuery.of(context).size.width / 2 - 90.w,
            bottom: 70.h,
            child: Text(
              'Create 30 office of you',
              style: AppStyles.title2TextStyle,
            ),
          ),
          Positioned(
            bottom: 25.h,
            left: MediaQuery.of(context).size.width / 2 - 35.w,
            child: GestureDetector(
              onTap: () {
                router.goNamed(AppViews.officePageRoute);
              },
              child: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(30.r)),
                child: const Text(
                  'Try office',
                  style: TextStyle(fontWeight: FontWeight.w400),
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}
