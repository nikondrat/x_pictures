import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class PopupImage extends StatelessWidget {
  final String url;
  final bool isProfile;
  const PopupImage({super.key, required this.url, required this.isProfile});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return SizedBox(
      height: MediaQuery.of(context).size.height * 0.6,
      child: AlertDialog(
        contentPadding: EdgeInsets.zero,
        backgroundColor: Colors.transparent,
        insetPadding: EdgeInsets.zero,
        content: Builder(
          builder: (context) {
            return Padding(
              padding: EdgeInsets.all(24.h),
              child: Container(
                width: MediaQuery.of(context).size.width,
                height: MediaQuery.of(context).size.height * 0.5,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(AppValues.kRadius),
                  image: DecorationImage(
                      image: CachedNetworkImageProvider(url),
                      alignment: FractionalOffset.topCenter,
                      fit: BoxFit.cover),
                ),
              ),
            );
          },
        ),
        actions: [
          SizedBox(
            height: 40.w,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Expanded(
                  flex: isProfile ? 6 : 5,
                  child: SizedBox(
                    // width: isProfile ? 190.w : 250.w,
                    child: ElevatedButton.icon(
                      style: ButtonStyle(
                          backgroundColor:
                              WidgetStateProperty.all(Colors.white),
                          shape:
                              WidgetStateProperty.all<RoundedRectangleBorder>(
                                  RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(
                                          AppValues.kRadius.r)))),
                      onPressed: () {},
                      icon: SvgPicture.asset(
                        Assets.icons.download,
                        color: AppColors.kAdditionalColor,
                        // width: 20.h,
                        // height: 20.h,
                      ),
                      label: Text(
                        t.photos.download,
                        style: textTheme.titleLarge!.copyWith(
                            fontSize: 10.sp,
                            color: colorScheme.onSecondary,
                            fontWeight: FontWeight.bold),
                        // style: TextStyle(
                        //     color: AppColors.kAdditionalColor,
                        //     fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
                Gap(6.h),
                Expanded(
                  child: Container(
                      decoration: BoxDecoration(
                          color: AppColors.kSecondaryAdditionallyColor,
                          borderRadius:
                              BorderRadius.circular(AppValues.kRadius)),
                      padding: EdgeInsets.symmetric(horizontal: 14.h),
                      child: SvgPicture.asset(
                        Assets.icons.share,
                        color: Colors.white,
                      )),
                ),
                if (isProfile) Gap(6.h),
                if (isProfile)
                  Expanded(
                    child: Container(
                        decoration: BoxDecoration(
                            color: AppColors.kSecondaryAdditionallyColor,
                            borderRadius:
                                BorderRadius.circular(AppValues.kRadius)),
                        padding: EdgeInsets.symmetric(horizontal: 14.h),
                        child: GestureDetector(
                          child: SvgPicture.asset(
                            Assets.icons.trashBinMinimalistic,
                            color: Colors.red,
                          ),
                        )),
                  )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
