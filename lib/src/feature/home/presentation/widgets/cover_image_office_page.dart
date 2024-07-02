import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';

class ImageItemOffice extends StatelessWidget {
  const ImageItemOffice({super.key});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(20.r),
      child: Stack(
        children: [
          CachedNetworkImage(
            imageUrl:
                'https://savilerowco.com/wp/wp-content/uploads/2017/02/11.jpg',
            fit: BoxFit.cover,
            width: double.maxFinite,
            height: 200.h,
          ),
          Positioned(
            bottom: 40.h,
            left: MediaQuery.of(context).size.width / 2.w - 20.w,
            child: Text('Office', style: AppStyles.title2TextStyle),
          ),
          Positioned(
            bottom: 30.h,
            left: MediaQuery.of(context).size.width / 2.w - 15.w,
            child: Text(
              '6 photos',
              style: TextStyle(
                fontSize: 10.sp,
                fontWeight: FontWeight.w400,
                color: const Color(0xff7C7C9B),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
