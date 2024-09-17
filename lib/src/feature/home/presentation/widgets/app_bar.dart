import 'package:auto_size_text/auto_size_text.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:svg_flutter/svg.dart';
import 'package:x_pictures/src/data.dart';

class AppBarHomeView extends StatelessWidget {
  final PackModel model;
  const AppBarHomeView({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    final PacksStore store = context.read();

    final CarouselSliderController controller = CarouselSliderController();

    return SizedBox(
      height: 400,
      child: Stack(
        fit: StackFit.expand,
        children: [
          CarouselSlider.builder(
            carouselController: controller,
            itemCount: model.images.length,
            itemBuilder: (context, index, realIndex) {
              return Row(
                children: [
                  Expanded(
                      child: ImageWithShader(
                    url: model.images[index].url,
                    colors: const [
                      AppColors.kBackgroundColor,
                      Colors.transparent,
                    ],
                  )),
                ],
              );
            },
            options: CarouselOptions(
              height: 400,
              viewportFraction: 1,
              autoPlay: true,
            ),
          ),
          // ImageWithShader(
          //     url: model.images.isNotEmpty
          //         ? model.images.first.url
          //         : 'https://images.livemint.com/img/2021/02/02/1140x641/hunters-race-MYbhN8KaaEc-unsplash_1612280206849_1612280227004.jpg'),
          SafeArea(
            child: Align(
              alignment: Alignment.topCenter,
              child: SvgPicture.asset(Assets.icons.x, width: 28),
            ),
          ),
          // Positioned(
          //   top: 40.h,
          //   left: MediaQuery.of(context).size.width / 2 - 10.w,
          //   child: SvgPicture.asset(AppIcons.xIcon),
          // ),
          //
          SafeArea(
            child: Align(
              alignment: Alignment.topRight,
              child: Padding(
                padding: EdgeInsets.only(right: 10.w),
                child: GestureDetector(
                  onTap: () {
                    context.pushNamed(AppViews.planView,
                        extra: {'continueAction': () {}});
                  },
                  child: SvgPicture.asset(
                    Assets.icons.pro,
                    width: 30,
                    height: 30,
                  ),
                ),
              ),
            ),
          ),

          // Positioned(
          //   top: 40,
          //   right: 20,
          //   child: SvgPicture.asset(
          //     AppIcons.proIcon,
          //     width: 65.w,
          //   ),
          // ),
          Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              AutoSizeText(
                t.homeView.title,
                style: textTheme.headlineSmall!.copyWith(
                  fontSize: 24.sp,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const Gap(AppValues.kPadding),
              GestureDetector(
                onTap: () {
                  store.setSelectedPack(model);
                  router.pushNamed(AppViews.officePageRoute, extra: {
                    'store': store,
                  });
                },
                child: Container(
                    padding:
                        EdgeInsets.symmetric(horizontal: 12.r, vertical: 10.r),
                    decoration: BoxDecoration(
                        color: colorScheme.secondary,
                        borderRadius:
                            BorderRadius.circular(AppValues.kRadius * 2)),
                    child: AutoSizeText(
                      t.homeView.try_office,
                      style: textTheme.titleMedium!.copyWith(
                          color: colorScheme.onSecondary,
                          fontWeight: FontWeight.bold),
                    )),
              ),
              const Gap(AppValues.kPadding * 2),
            ],
          ),

          // Positioned(
          //   left: MediaQuery.of(context).size.width / 2 - 90.w,
          //   bottom: 70.h,
          //   child: Text(
          //     'Create 30 office of you',
          //     style: AppStyles.title2TextStyle,
          //   ),
          // ),
          // Positioned(
          //   bottom: 25.h,
          //   left: MediaQuery.of(context).size.width / 2 - 35.w,
          //   child: GestureDetector(
          //     onTap: () {
          //       router.goNamed(AppViews.officePageRoute);
          //     },
          //     child: Container(
          //       padding: const EdgeInsets.all(8),
          //       decoration: BoxDecoration(
          //           color: Colors.white,
          //           borderRadius: BorderRadius.circular(30.r)),
          //       child: Text(
          //         'Try office',
          //         style: TextStyle(
          //             fontWeight: FontWeight.w400,
          //             color: colorScheme.onSecondary),
          //       ),
          //     ),
          //   ),
          // )
        ],
      ),
    );
  }
}
