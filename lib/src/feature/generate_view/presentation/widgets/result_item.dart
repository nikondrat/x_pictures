import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class ResultItem extends StatelessWidget {
  final String url;
  final double windowHeight;
  final bool needPro;
  const ResultItem(
      {super.key,
      required this.url,
      required this.windowHeight,
      this.needPro = false});

  @override
  Widget build(BuildContext context) {
    return needPro
        ? _Pro(
            windowHeight: windowHeight,
          )
        : Padding(
            padding:
                const EdgeInsets.symmetric(horizontal: AppValues.kPadding / 4),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(AppValues.kRadius.r),
              child: CachedNetworkImage(
                imageUrl: url,
                fit: BoxFit.cover,
                height: 70.h,
                // width: windowHeight * .07,
              ),
            ),
          );
  }
}

class _Pro extends StatelessWidget {
  final double windowHeight;
  const _Pro({
    required this.windowHeight,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 70.h,
      margin: const EdgeInsets.all(AppValues.kPadding / 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppValues.kRadius.r),
        color: AppColors.kSecondaryAdditionallyColor,
      ),
      child: Center(child: SvgPicture.asset(Assets.icons.pro)),
    );
  }
}
