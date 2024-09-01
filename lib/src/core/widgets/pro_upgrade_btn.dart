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

    return ClipRRect(
      borderRadius: BorderRadius.circular(AppValues.kRadius.r),
      child: Container(
        height: 80.h,
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: [
            colorScheme.primary,
            AppColors.kPrimaryAdditionallyColor
          ],
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter),
        ),
        child: Stack(
          children: [
            Positioned(
                left: 0.w,
                top: 20.h,
                child: SvgPicture.asset(
                    Assets.icons.bannerProElem01),
            ),
            Positioned(
                right: 0.w,
                bottom: 0.h,
                child: SvgPicture.asset(Assets.icons.bannerProElem02),
            ),
            ListTile(
              title: Padding(
                padding: EdgeInsets.symmetric(vertical: 8.h),
                child: Text(
                    t.common.upgrade_pro,
                style: textTheme.titleLarge!.copyWith(
                  fontSize: 14.sp,
                  fontWeight: FontWeight.bold
                ),
                ),
              ),
              subtitle: Text(t.common.banner_pro_text),
              trailing: Padding(
                padding: EdgeInsets.only(top: 8.h),
                child: ElevatedButton(
                    onPressed: onPressed,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.kSecondaryColor
                    ),
                    child: Text(
                        t.common.banner_pro_btn_text,
                    style: textTheme.titleSmall!.copyWith(
                      fontSize: 12.sp,
                      color: AppColors.kBackgroundColor,
                      fontWeight: FontWeight.w400,
                    ),)),
              ),
            )
          ],
        )
      ),
    );
  }
}

