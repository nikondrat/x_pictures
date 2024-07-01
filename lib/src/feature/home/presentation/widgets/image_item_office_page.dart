import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:cached_network_image/cached_network_image.dart';

class ImageItemOfficePage extends StatelessWidget {
  const ImageItemOfficePage({super.key});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(10.r),
      child: CachedNetworkImage(
        width: 160.w,
        height: 190.h,
        imageUrl:
            'https://savilerowco.com/wp/wp-content/uploads/2017/02/11.jpg',
        fit: BoxFit.cover,
      ),
    );
  }
}
