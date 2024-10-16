import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';

class UploadingPhotosPage extends StatefulWidget {
  const UploadingPhotosPage({super.key});

  @override
  State<UploadingPhotosPage> createState() => _UploadingPhotosPageState();
}

class _UploadingPhotosPageState extends State<UploadingPhotosPage> {
  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;
    final LoraStore loraStore = context.watch<LoraStore>();

    // bool haveError = true;

    return Scaffold(
        // appBar: const CustomAppBar(textName: 'Uploading photos'),
        appBar: AppBar(
            leading: const CustomBackButton(),
            title: Text(
              t.homeView.uploading_photos,
              style: textTheme.bodyMedium!.copyWith(
                fontWeight: FontWeight.w700,
                fontSize: 17,
              ),
            )),
        // floatingActionButton: CustomFloatingButton(
        //     buttonName: 'Continue',
        //     onTap: () => router
        //         .goNamed(AppViews.genderView, extra: {"model": widget.model})),
        body: AppBody(
            builder: (windowWidth, windowHeight, __) => SafeArea(
                    child: Stack(fit: StackFit.expand, children: [
                  CustomScrollView(
                    slivers: <Widget>[
                      SliverToBoxAdapter(
                        child: Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: 15.w, vertical: 15.h),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              AutoSizeText(
                                'Step 2 of 3',
                                minFontSize: 8,
                                style: AppStyles.subTitleTextStyle.copyWith(
                                  fontSize: 6.sp,
                                ),
                              ),
                              SizedBox(
                                height: 5.h,
                              ),
                              Padding(
                                padding: EdgeInsets.only(right: 50.w),
                                child: AutoSizeText(
                                  'Your photos have been processed',
                                  style: textTheme.bodyLarge!.copyWith(
                                      fontSize: 17.sp,
                                      fontWeight: FontWeight.bold),
                                ),
                              ),
                              SizedBox(
                                height: 5.h,
                              ),
                              AutoSizeText(
                                'Description',
                                style: textTheme.bodyMedium!.copyWith(
                                    fontSize: 14.sp,
                                    color: AppColors.kOutlineColor),
                              ),
                              SizedBox(
                                height: 20.h,
                              ),
                              AutoSizeText(
                                'Your photos',
                                style: AppStyles.title2TextStyle
                                    .copyWith(fontSize: 17.sp),
                              ),
                              Observer(builder: (context) {
                                if (!loraStore.canGenerateLora) {
                                  return AutoSizeText(
                                    'Maximum of 12 photos can be uploaded.',
                                    style: textTheme.bodyLarge!
                                        .copyWith(color: colorScheme.error),
                                  );
                                }
                                return const SizedBox.shrink();
                              }),
                            ],
                          ),
                        ),
                      ),
                      const UploadingPhotosBody(),
                      Observer(builder: (_) {
                        if (loraStore.photosLength > 7) {
                          return SliverPadding(
                            padding: EdgeInsets.only(
                                left: 15.w, right: 15.w, bottom: 120.h),
                            sliver: SliverToBoxAdapter(
                              child: AutoSizeText(
                                t.homeView.not_comply,
                                style: textTheme.bodyLarge!
                                    .copyWith(color: colorScheme.error),
                              ),
                            ),
                          );
                        }
                        return const SliverToBoxAdapter();
                      })
                    ],
                  ),
                  Align(
                    alignment: Alignment.bottomCenter,
                    child: Padding(
                      padding: HorizontalSpacing.centered(windowWidth) +
                          EdgeInsets.only(bottom: 20.h),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          GradientButton(
                              onPressed: () {
                                router.pushNamed(AppViews.genderView);
                              },
                              text: t.common.continue_action),
                        ],
                      ),
                    ),
                  ),
                ]))));
  }

  // Widget uploadPhoto(int index, BuildContext context) {
  //   // if (index < imageFiles.length) {
  //   //   return ImageItemUploadingPhotosPage(imageFile: imageFiles[index]);
  //   // } else
  //   if (index == imageFiles.length) {
  //     return GestureDetector(
  //       onTap: () async {
  //         if (imageFiles.length < 12) {
  //           final pickedFile =
  //               await picker.pickImage(source: ImageSource.gallery);
  //           if (pickedFile != null) {
  //             setState(() {
  //               imageFiles.add(File(pickedFile.path));
  //             });
  //           }
  //         } else {
  //           ScaffoldMessenger.of(context).showSnackBar(
  //             const SnackBar(
  //               content: Text('Maximum of 12 photos can be uploaded.'),
  //             ),
  //           );
  //         }
  //       },
  //       child: Container(
  //         alignment: Alignment.center,
  //         decoration: BoxDecoration(
  //           color: const Color(0xff0D1120),
  //           borderRadius: BorderRadius.circular(8.r),
  //         ),
  //         child: const Icon(
  //           Icons.add,
  //           color: Colors.white,
  //           size: 32,
  //         ),
  //       ),
  //     );
  //   } else {
  //     return const SizedBox.shrink();
  //   }
  // }
}
