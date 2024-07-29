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
              padding: const EdgeInsets.all(AppValues.kPadding),
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
          Row(
            children: [
              Expanded(
                child: SizedBox(
                  // width: isProfile ? 190.w : 250.w,
                  height: 50.h,
                  child: ElevatedButton.icon(
                    style: ButtonStyle(
                        backgroundColor: WidgetStateProperty.all(Colors.white),
                        shape: WidgetStateProperty.all<RoundedRectangleBorder>(
                            RoundedRectangleBorder(
                                borderRadius:
                                    BorderRadius.circular(AppValues.kRadius)))),
                    onPressed: () {},
                    icon: SvgPicture.asset(
                      Assets.icons.download,
                      color: AppColors.kAdditionalColor,
                      width: 20.h,
                      height: 20.h,
                    ),
                    label: Text(
                      t.photos.download,
                      style: textTheme.headlineSmall!.copyWith(
                          color: colorScheme.onSecondary,
                          fontWeight: FontWeight.bold),
                      // style: TextStyle(
                      //     color: AppColors.kAdditionalColor,
                      //     fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              ),
              const Gap(AppValues.kPadding),
              Container(
                  decoration: BoxDecoration(
                      color: AppColors.kSecondaryAdditionallyColor,
                      borderRadius: BorderRadius.circular(AppValues.kRadius)),
                  width: 50.h,
                  height: 50.h,
                  padding: EdgeInsets.all(16.w),
                  child: GestureDetector(
                    child: SvgPicture.asset(
                      Assets.icons.share,
                      color: Colors.white,
                    ),
                  )),
              if (isProfile) const Gap(AppValues.kPadding),
              if (isProfile)
                Container(
                    decoration: BoxDecoration(
                        color: AppColors.kSecondaryAdditionallyColor,
                        borderRadius: BorderRadius.circular(AppValues.kRadius)),
                    width: 50.h,
                    height: 50.h,
                    padding: EdgeInsets.all(16.w),
                    child: GestureDetector(
                      child: SvgPicture.asset(
                        Assets.icons.trashBinMinimalistic,
                        width: 20.h,
                        height: 20.h,
                      ),
                    ))
            ],
          ),
        ],
      ),
    );
  }
}
