import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';

class GenderView extends StatelessWidget {
  const GenderView({super.key});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return ChangeNotifierProvider(
      create: (context) => GenderState(),
      child: Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            title: Text(
              t.gender.title,
              style: textTheme.bodyMedium!.copyWith(
                fontWeight: FontWeight.w700,
                fontSize: 17,
              ),
            ),
          ),
          // floatingActionButton:
          //     Consumer<GenderState>(builder: (context, consumerValue, child) {
          //   return Padding(
          //     padding: EdgeInsets.only(left: 30.w),
          //     child: SizedBox(
          //       height: 50.h,
          //       child: GradientButton(
          //         onPressed: () {
          //           router.goNamed(AppViews.planView, extra: {"model": model});
          //         },
          //         text: 'Continue',
          //         isEnabled: consumerValue.isSelected,
          //       ),
          //     ),
          //   );
          // }),
          body: AppBody(
              builder: (windowWidth, windowHeight, __) => Consumer<GenderState>(
                  builder: (context, consumerValue, child) => SafeArea(
                          child: Stack(fit: StackFit.expand, children: [
                        Padding(
                            padding: EdgeInsets.symmetric(
                                horizontal: 15.w, vertical: 15.h),
                            child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  AutoSizeText(
                                    t.template.step_third,
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
                                    child: AutoSizeText(
                                      t.gender.title,
                                      style: AppStyles.head1TextStyle.copyWith(
                                        fontSize: 17.sp,
                                      ),
                                    ),
                                  ),
                                  SizedBox(
                                    height: 5.h,
                                  ),
                                  AutoSizeText(
                                    t.gender.description,
                                    style: AppStyles.subTitleTextStyle.copyWith(
                                      fontSize: 14.sp,
                                    ),
                                  ),
                                  SizedBox(
                                    height: 20.h,
                                  ),
                                  RadioButton(
                                      text: t.gender.female,
                                      isSelected:
                                          consumerValue.isSelectedList[0],
                                      value: Gender.female,
                                      groupValue: consumerValue.currentGender,
                                      onChanged: (value) {
                                        consumerValue
                                            .changeCurrentGender(value);
                                        consumerValue
                                            .setTrueToIsSelectedList(0);
                                      }),
                                  RadioButton(
                                      text: t.gender.male,
                                      isSelected:
                                          consumerValue.isSelectedList[1],
                                      value: Gender.male,
                                      groupValue: consumerValue.currentGender,
                                      onChanged: (value) {
                                        consumerValue
                                            .changeCurrentGender(value);
                                        consumerValue
                                            .setTrueToIsSelectedList(1);
                                      }),
                                  RadioButton(
                                      text: t.gender.other,
                                      isSelected:
                                          consumerValue.isSelectedList[2],
                                      value: Gender.other,
                                      groupValue: consumerValue.currentGender,
                                      onChanged: (value) {
                                        consumerValue
                                            .changeCurrentGender(value);
                                        consumerValue
                                            .setTrueToIsSelectedList(2);
                                      }),
                                ])),
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
                                      router.pushNamed(AppViews.planView);
                                    },
                                    text: t.common.continue_action),
                              ],
                            ),
                          ),
                        ),
                      ]))))),
    );
  }
}
