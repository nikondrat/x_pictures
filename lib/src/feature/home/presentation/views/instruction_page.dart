import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class InstructionPage extends StatelessWidget {
  final PacksStore store;
  const InstructionPage({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

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
          title: Text(
            t.homeView.instruction,
            style: textTheme.headlineSmall!
                .copyWith(fontWeight: FontWeight.w700, fontSize: 10.sp),
          ),
        ),
        body: AppBody(
            builder: (windowWidth, windowHeight, __) => SafeArea(
                    child: Stack(fit: StackFit.expand, children: [
                  SingleChildScrollView(
                    child: Padding(
                      padding: EdgeInsets.symmetric(
                          horizontal: 15.w, vertical: 15.h),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Step 1 of 3',
                            style: AppStyles.subTitleTextStyle.copyWith(
                              fontSize: 6.sp,
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
                                  fontSize: 12.sp, fontWeight: FontWeight.bold),
                            ),
                          ),
                          SizedBox(
                            height: 5.h,
                          ),
                          Text(
                            'Your photos are completely confidential and will only be used to create avatars.',
                            style: textTheme.bodyMedium!.copyWith(
                                fontSize: 9.sp, color: AppColors.kOutlineColor),
                          ),
                          SizedBox(
                            height: 20.h,
                          ),
                          Text(
                            'Good photos',
                            style: textTheme.bodyLarge!.copyWith(
                                fontSize: 10.sp, fontWeight: FontWeight.bold),
                          ),
                          SizedBox(
                            height: 5.h,
                          ),
                          Text(
                              'Excellent quality, good angle, one face, different backgrounds, lighting, etc',
                              style: textTheme.bodyMedium!.copyWith(
                                  fontSize: 9.sp,
                                  color: AppColors.kOutlineColor)),
                          SizedBox(
                            height: 5.h,
                          ),
                          SizedBox(
                            height: 60.h,
                            child: ListView.builder(
                              scrollDirection: Axis.horizontal,
                              itemCount: 4,
                              itemBuilder: (BuildContext context, int index) {
                                return Image.asset(AppImages.goodPhotoExa);
                              },
                            ),
                          ),
                          SizedBox(
                            height: 5.h,
                          ),
                          Text(
                            'Bad photos',
                            style: textTheme.bodyLarge!.copyWith(
                                fontSize: 10.sp, fontWeight: FontWeight.bold),
                          ),
                          SizedBox(
                            height: 5.h,
                          ),
                          Text(
                              'A lot of faces, glasses, poor quality, nudity, kids, etc.',
                              style: textTheme.bodyMedium!.copyWith(
                                  fontSize: 9.sp,
                                  color: AppColors.kOutlineColor)),
                          SizedBox(
                            height: 5.h,
                          ),
                          SizedBox(
                              height: 60.h,
                              child: ListView(
                                scrollDirection: Axis.horizontal,
                                children: [
                                  Padding(
                                    padding: EdgeInsets.only(right: 10.r),
                                    child: Image.asset(AppImages.badPhotoExa1),
                                  ),
                                  Padding(
                                    padding: EdgeInsets.only(right: 10.r),
                                    child: Image.asset(AppImages.badPhotoExa2),
                                  ),
                                  Padding(
                                    padding: EdgeInsets.only(right: 10.r),
                                    child: Image.asset(AppImages.badPhotoExa3),
                                  ),
                                  Padding(
                                    padding: EdgeInsets.only(right: 10.r),
                                    child: Image.asset(AppImages.badPhotoExa2),
                                  ),
                                ],
                              )),
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
                          EdgeInsets.only(bottom: AppValues.kPadding * 2),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          GradientButton(
                              onPressed: () {
                                router.pushNamed(
                                    AppViews.uploadingPhotosPageRoute,
                                    extra: {'store': store});
                              },
                              text: t.homeView.upload_photos),
                        ],
                      ),
                    ),
                  ),
                ]))));
  }
}
