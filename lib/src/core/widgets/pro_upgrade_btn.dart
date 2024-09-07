import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/core/constant/constant.dart';

class ProUpgradeBtn extends StatelessWidget {
  final Function() onPressed;

  const ProUpgradeBtn({
    super.key,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return GestureDetector(
      onTap: onPressed,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(AppValues.kRadius.r),
        child: SizedBox(
          height: 90,
          child: DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(colors: [
                  colorScheme.primary,
                  AppColors.kPrimaryAdditionallyColor
                ], begin: Alignment.topCenter, end: Alignment.bottomCenter),
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  Positioned(
                    left: 0.w,
                    top: 14.h,
                    child: SvgPicture.asset(Assets.icons.bannerProElem01),
                  ),
                  Positioned(
                    right: 0.w,
                    bottom: 0.h,
                    child: SvgPicture.asset(Assets.icons.bannerProElem02),
                  ),
                  ListTile(
                      contentPadding: const EdgeInsets.symmetric(
                          horizontal: AppValues.kPadding),
                      title: Text(
                        t.common.upgrade_pro,
                        style: textTheme.titleLarge!.copyWith(
                            fontSize: 14.sp, fontWeight: FontWeight.bold),
                      ),
                      subtitle: Padding(
                        padding: const EdgeInsets.only(
                          top: AppValues.kPadding / 3,
                        ),
                        child: Text(t.common.banner_pro_text),
                      ),
                      trailing: DecoratedBox(
                        decoration: BoxDecoration(
                            color: colorScheme.onPrimary,
                            borderRadius:
                                BorderRadius.circular(AppValues.kRadius * 2.r)),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 16, vertical: 8),
                          child: Text(t.common.banner_pro_btn_text,
                              style: textTheme.titleSmall!.copyWith(
                                color: colorScheme.onSecondary,
                                fontWeight: FontWeight.w400,
                                fontSize: 12.sp,
                              )),
                        ),
                      )
                      // ElevatedButton(
                      //     onPressed: onPressed,
                      //     style: ElevatedButton.styleFrom(
                      //         backgroundColor: AppColors.kSecondaryColor),
                      //     child: Text(
                      //       t.common.banner_pro_btn_text,
                      //       style: textTheme.titleSmall!.copyWith(
                      //         fontSize: 12.sp,
                      //         color: AppColors.kBackgroundColor,
                      //         fontWeight: FontWeight.w400,
                      //       ),
                      //     )),
                      )
                ],
              )),
        ),
      ),
    );
  }
}
