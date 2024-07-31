import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class ProfilesWidget extends StatelessWidget {
  const ProfilesWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Container(
      margin: const EdgeInsets.only(bottom: AppValues.kPadding),
      decoration: BoxDecoration(
        color: AppColors.kSecondaryAdditionallyColor,
        borderRadius: BorderRadius.circular(AppValues.kRadius),
      ),
      padding: const EdgeInsets.all(AppValues.kPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          AutoSizeText(t.profile.my_ai_profiles,
              style:
                  textTheme.titleMedium!.copyWith(fontWeight: FontWeight.bold)),
          const Gap(AppValues.kPadding / 2),
          Row(
            children: [
              'https://c.wallhere.com/photos/a0/1c/johannes_strate_skarf_man_face_field-776717.jpg!d',
              'https://c.wallhere.com/photos/a0/1c/johannes_strate_skarf_man_face_field-776717.jpg!d',
            ].mapIndexed((i, e) {
              final bool isSelected = i == 0;

              return Padding(
                padding: EdgeInsets.only(right: 8.r),
                child: Stack(
                  alignment: Alignment.bottomRight,
                  children: [
                    Container(
                      width: 70.h,
                      height: 70.h,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: isSelected
                            ? Border.all(
                                color: AppColors.kPrimaryColor, width: 2)
                            : null,
                        image: DecorationImage(
                            image: CachedNetworkImageProvider(e),
                            fit: BoxFit.cover),
                      ),
                    ),
                    if (isSelected)
                      Container(
                        width: 16,
                        height: 16,
                        margin: EdgeInsets.all(1.r),
                        decoration: const BoxDecoration(
                          color: AppColors.kPrimaryColor,
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          Icons.done,
                          size: 6.r,
                        ),
                      ),
                  ],
                ),
              );
            }).toList(),
          )
        ],
      ),
    );
  }
}
