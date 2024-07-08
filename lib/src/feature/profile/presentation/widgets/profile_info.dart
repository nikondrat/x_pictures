import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class ProfileInfoWidget extends StatelessWidget {
  final String name;
  final String email;
  final String url;
  final Function() onTap;
  const ProfileInfoWidget(
      {super.key,
      required this.name,
      required this.email,
      required this.url,
      required this.onTap});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(AppValues.kPadding),
        decoration: BoxDecoration(
            color: AppColors.kSecondaryAdditionallyColor,
            borderRadius: BorderRadius.circular(AppValues.kRadius)),
        child: Row(
          children: [
            CircleAvatar(
              radius: 30.h,
              backgroundImage: CachedNetworkImageProvider(url),
            ),
            const Gap(AppValues.kPadding),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  AutoSizeText(
                    name,
                    style: textTheme.titleLarge,
                    maxLines: 2,
                  ),
                  const Gap(AppValues.kPadding / 3),
                  AutoSizeText(
                    email,
                    style: textTheme.titleMedium!
                        .copyWith(color: AppColors.kOutlineColor),
                    maxLines: 1,
                  ),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios)
          ],
        ),
      ),
    );
  }
}
