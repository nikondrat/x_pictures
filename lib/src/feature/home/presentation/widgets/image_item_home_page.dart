import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class ImageItemHomePage extends StatelessWidget {
  const ImageItemHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 100.w,
      height: 130.h,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(10.r),
        child: Stack(
          children: [
            CachedNetworkImage(
              width: 100.w,
              height: 130.h,
              imageUrl:
                  'https://savilerowco.com/wp/wp-content/uploads/2017/02/11.jpg',
              fit: BoxFit.cover,
            ),
            Positioned(
              bottom: 20.h,
              left: 10.w,
              child: Text(
                'Street casual',
                style: TextStyle(
                  fontSize: 10.sp,
                  fontWeight: FontWeight.w400,
                  color: const Color(0xffFFFFFF),
                ),
              ),
            ),
            Positioned(
              bottom: 7.h,
              left: 10.w,
              child: Text(
                '6 photos',
                style: TextStyle(
                  fontSize: 9.sp,
                  fontWeight: FontWeight.w400,
                  color: const Color(0xff7C7C9B),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
