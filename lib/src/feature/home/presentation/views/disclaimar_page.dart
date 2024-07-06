import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/core/constant/images.dart';
import 'package:x_pictures/src/data.dart';

class DisclaimarPage extends StatelessWidget {
  final StyleModel model;
  const DisclaimarPage({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Scaffold(
        appBar: AppBar(
          leading: const CustomBackButton(),
          title: Text(
            t.homeView.disclaimer,
            style:
                textTheme.headlineSmall!.copyWith(fontWeight: FontWeight.w700),
          ),
        ),
        // floatingActionButton: CustomFloatingButton(
        //   buttonName: 'Get started',
        //   onTap: () {
        //     router.goNamed(AppViews.instructionPageRoute,
        //         extra: {"model": model});
        //   },
        // ),
        body: AppBody(
            builder: (windowWidth, windowHeight, __) => SafeArea(
                    child: Stack(fit: StackFit.expand, children: [
                  SingleChildScrollView(
                    child: Padding(
                      padding: HorizontalSpacing.centered(windowWidth) +
                          const EdgeInsets.only(top: AppValues.kPadding),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          SizedBox(
                            width: windowWidth,
                            height: windowHeight * .5,
                            child: ClipRRect(
                              borderRadius:
                                  BorderRadius.circular(AppValues.kRadius),
                              child: Image.asset(
                                AppImages.testImage,
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                          const Gap(AppValues.kPadding * 2),
                          // SizedBox(
                          //   height: 20.h,
                          // ),
                          AutoSizeText(
                            '${t.homeView.how_it_works}?',
                            style: textTheme.headlineSmall!.copyWith(
                              fontWeight: FontWeight.w700,
                            ),
                            // style: AppStyles.title2TextStyle,
                          ),
                          const Gap(AppValues.kPadding),
                          // SizedBox(
                          //   height: 10.h,
                          // ),
                          AutoSizeText(
                            'Описание правил',
                            style: textTheme.bodyLarge!.copyWith(
                              color: AppColors.kOutlineColor,
                            ),
                            // style: AppStyles.subTitleTextStyle,
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
                      child: SizedBox(
                          height: 80,
                          child: GradientButton(
                              onPressed: () {
                                router.goNamed(AppViews.instructionPageRoute,
                                    extra: {'model': model});
                              },
                              text: t.homeView.get_started)),
                    ),
                  ),
                ]))));
  }
}
