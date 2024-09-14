import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class InstructionPage extends StatelessWidget {
  const InstructionPage({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    final List<AssetGenImage> badPhotos = [
      Assets.images.photos.badly1,
      Assets.images.photos.badly2,
      Assets.images.photos.badly3,
      Assets.images.photos.badly4,
      Assets.images.photos.badly5,
      Assets.images.photos.badly6,
    ];

    final List<AssetGenImage> goodPhotos = [
      Assets.images.photos.goodly1,
      Assets.images.photos.goodly2,
      Assets.images.photos.goodly3,
      Assets.images.photos.goodly4,
      Assets.images.photos.goodly5,
      Assets.images.photos.goodly6,
    ];

    return Scaffold(
        // floatingActionButton: CustomFloatingButton(
        //     buttonName: 'Upload photos',
        //     onTap: () {
        //       router.goNamed(AppViews.uploadingPhotosPageRoute,
        //           extra: {'model': model});
        //     }),
        // appBar: const CustomAppBar(textName: 'Instruction'),
        appBar: AppBar(
          leading: const CustomBackButton(),
          title: AutoSizeText(
            t.homeView.instruction,
            style: textTheme.bodyMedium!.copyWith(
              fontWeight: FontWeight.w700,
              fontSize: 17,
            ),
          ),
        ),
        body: AppBody(
            builder: (windowWidth, windowHeight, __) => SafeArea(
                    child: Stack(
                        // fit: StackFit.expand,
                        children: [
                      SingleChildScrollView(
                        child: Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: 15.w, vertical: 15.h),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              AutoSizeText(
                                'Step 1 of 3',
                                minFontSize: 8,
                                style: AppStyles.subTitleTextStyle.copyWith(
                                  fontSize: 8.sp,
                                ),
                              ),
                              SizedBox(
                                height: 5.h,
                              ),
                              Padding(
                                padding: EdgeInsets.only(right: 50.w),
                                child: Text(
                                  'Pick 8-12 photos of yourself',
                                  style: textTheme.bodyLarge!.copyWith(
                                      fontSize: 17.sp,
                                      fontWeight: FontWeight.bold),
                                ),
                              ),
                              SizedBox(
                                height: 5.h,
                              ),
                              AutoSizeText(
                                'Your photos are completely confidential and will only be used to create avatars.',
                                style: textTheme.bodyMedium!.copyWith(
                                    fontSize: 14.sp,
                                    color: AppColors.kOutlineColor),
                              ),
                              SizedBox(
                                height: 20.h,
                              ),
                              AutoSizeText(
                                'Good photos',
                                style: textTheme.bodyLarge!.copyWith(
                                    fontSize: 17.sp,
                                    fontWeight: FontWeight.bold),
                              ),
                              SizedBox(
                                height: 5.h,
                              ),
                              AutoSizeText(
                                  'Excellent quality, good angle, one face, different backgrounds, lighting, etc',
                                  style: textTheme.bodyMedium!.copyWith(
                                      fontSize: 14.sp,
                                      color: AppColors.kOutlineColor)),
                              SizedBox(
                                height: 20.h,
                              ),
                              SizedBox(
                                height: 100.h,
                                child: ListView.builder(
                                  scrollDirection: Axis.horizontal,
                                  itemCount: goodPhotos.length,
                                  itemBuilder:
                                      (BuildContext context, int index) {
                                    return Padding(
                                      padding: EdgeInsets.only(right: 10.r),
                                      child: PhotoWidget(
                                          isBadPhoto: false,
                                          path: goodPhotos[index].path),
                                    );
                                  },
                                ),
                              ),
                              SizedBox(
                                height: 20.h,
                              ),
                              AutoSizeText(
                                'Bad photos',
                                style: textTheme.bodyLarge!.copyWith(
                                    fontSize: 17.sp,
                                    fontWeight: FontWeight.bold),
                              ),
                              SizedBox(
                                height: 5.h,
                              ),
                              AutoSizeText(
                                  'A lot of faces, glasses, poor quality, nudity, kids, etc.',
                                  style: textTheme.bodyMedium!.copyWith(
                                      fontSize: 14.sp,
                                      color: AppColors.kOutlineColor)),
                              SizedBox(
                                height: 20.h,
                              ),
                              SizedBox(
                                height: 100.h,
                                child: ListView.builder(
                                  scrollDirection: Axis.horizontal,
                                  itemCount: badPhotos.length,
                                  itemBuilder:
                                      (BuildContext context, int index) {
                                    return Padding(
                                      padding: EdgeInsets.only(right: 10.r),
                                      child: PhotoWidget(
                                          path: badPhotos[index].path),
                                    );
                                  },
                                ),
                              ),
                              SizedBox(
                                height: 50.h,
                              ),
                            ],
                          ),
                        ),
                      ),
                      Align(
                        alignment: Alignment.bottomCenter,
                        child: Padding(
                          padding: HorizontalSpacing.centered(windowWidth) +
                              const EdgeInsets.only(
                                  bottom: AppValues.kPadding * 2),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              GradientButton(
                                  onPressed: () {
                                    router.pushNamed(
                                      AppViews.uploadingPhotosPageRoute,
                                    );
                                  },
                                  text: t.homeView.upload_photos),
                            ],
                          ),
                        ),
                      ),
                    ]))));
  }
}
