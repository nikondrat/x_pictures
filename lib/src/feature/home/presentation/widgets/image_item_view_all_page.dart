import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:x_pictures/src/core/constant/styles.dart';

class ImageItemViewAllPage extends StatelessWidget {
  const ImageItemViewAllPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        ClipRRect(
          borderRadius: BorderRadius.circular(10.r),
          child: CachedNetworkImage(
            width: 160.w,
            height: 190.h,
            imageUrl:
                'https://savilerowco.com/wp/wp-content/uploads/2017/02/11.jpg',
            fit: BoxFit.cover,
          ),
        ),
        Positioned(
          bottom: 20.h,
          left: 10.w,
          child: Text(
            'Street casual',
            style: AppStyles.subTitleTextStyle.copyWith(
              color: const Color(0xffFFFFFF),
            ),
          ),
        ),
        Positioned(
          bottom: 7.h,
          left: 10.w,
          child: Text(
            '6 photos',
            style: AppStyles.subTitleTextStyle.copyWith(
              fontSize: 10.sp,
            ),
          ),
        ),
      ],
    );
  }
}
