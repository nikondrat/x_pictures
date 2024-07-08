import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/data.dart';

class CoverImagePlanPage extends StatelessWidget {
  const CoverImagePlanPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.only(
        bottomLeft: Radius.circular(20.r),
        bottomRight: Radius.circular(20.r),
      ),
      child: Stack(
        children: [
          Image.asset(
            AppImages.bannerImage,
            width: MediaQuery.of(context).size.width,
            height: MediaQuery.of(context).size.height * 0.4,
            fit: BoxFit.cover,
          ),
          Positioned(top: 20.h, left: 10.w, child: CustomBackButton())
        ],
      ),
    );
  }
}
