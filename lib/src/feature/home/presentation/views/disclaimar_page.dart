import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class DisclaimarPage extends StatelessWidget {
  const DisclaimarPage({super.key});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    return Scaffold(
        appBar: AppBar(
          leading: const CustomBackButton(),
          title: Text(
            t.homeView.disclaimer,
            style: textTheme.bodyMedium!.copyWith(
              fontWeight: FontWeight.w700,
              fontSize: 17,
            ),
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
                                Assets.images.testimage.path,
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
                          const EdgeInsets.only(bottom: AppValues.kPadding * 2),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          GradientButton(
                              onPressed: () {
                                router.pushNamed(AppViews.instructionPageRoute);
                              },
                              text: t.homeView.get_started),
                        ],
                      ),
                    ),
                  ),
                ]))));
  }
}
