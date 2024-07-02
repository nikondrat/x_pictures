import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
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
              borderRadius: BorderRadius.circular(AppValues.kRadius),
              child: CachedNetworkImage(
                imageUrl: url,
                fit: BoxFit.cover,
                height: windowHeight * .06,
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
      height: windowHeight * .06,
      margin: const EdgeInsets.all(AppValues.kPadding / 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(AppValues.kRadius),
        color: AppColors.kSecondaryAdditionallyColor,
      ),
      child: Center(child: SvgPicture.asset(Assets.icons.pro)),
    );
  }
}
