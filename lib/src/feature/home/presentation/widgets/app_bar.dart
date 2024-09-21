import 'package:auto_size_text/auto_size_text.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
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
              onPageChanged: (index, reason) {
                store.setCarouselIndex(index);
              },
            ),
          ),
          SafeArea(
            child: Align(
              alignment: Alignment.topCenter,
              child: SvgPicture.asset(Assets.icons.x, width: 28),
            ),
          ),
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
              Observer(builder: (context) {
                return Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Stack(
                      alignment: Alignment.center,
                      children: [
                        const SizedBox(
                          width: 140,
                          height: 2,
                          child: DecoratedBox(
                              decoration: BoxDecoration(
                            color: Colors.grey,
                          )),
                        ),
                        TweenAnimationBuilder<double>(
                            tween: Tween<double>(
                              begin: store.carouselIndex *
                                  (120 / (model.images.length - 1)),
                              end: store.carouselIndex *
                                  (120 / (model.images.length - 1)),
                            ),
                            duration: const Duration(
                                milliseconds: 300), // Длительность анимации
                            builder: (context, value, child) => Positioned(
                                  left: value,
                                  child: const SizedBox(
                                    width: 20,
                                    height: 2,
                                    child: DecoratedBox(
                                        decoration: BoxDecoration(
                                      color: AppColors.kSecondaryColor,
                                    )),
                                  ),
                                )),
                        SliderTheme(
                            data: SliderTheme.of(context).copyWith(
                              trackHeight: 0,
                              thumbShape: const RoundSliderThumbShape(
                                  enabledThumbRadius: 0),
                              overlayShape: const RoundSliderOverlayShape(
                                  overlayRadius: 0),
                            ),
                            child: Slider(
                              value: store.carouselIndex.toDouble(),
                              min: 0,
                              max: model.images.length.toDouble(),
                              onChanged: (value) {},
                            ))
                      ],
                    ),
                  ],
                );
              }),
              const Gap(AppValues.kPadding),
            ],
          ),
        ],
      ),
    );
  }
}
