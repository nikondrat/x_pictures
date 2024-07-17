import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/feature/template_view/enum/enum.dart';

class GenderView extends StatelessWidget {
  final PackModel model;
  const GenderView({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => GenderState(),
      child: Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            title: Text(t.gender.title),
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
                                  Text(
                                    t.template.step_third,
                                    style: AppStyles.subTitleTextStyle.copyWith(
                                      fontSize: 10.sp,
                                    ),
                                  ),
                                  SizedBox(
                                    height: 5.h,
                                  ),
                                  Padding(
                                    padding: EdgeInsets.only(right: 50.w),
                                    child: Text(
                                      t.gender.title,
                                      style: AppStyles.head1TextStyle,
                                    ),
                                  ),
                                  SizedBox(
                                    height: 5.h,
                                  ),
                                  Text(
                                    t.gender.description,
                                    style: AppStyles.subTitleTextStyle.copyWith(
                                      fontSize: 17.sp,
                                    ),
                                  ),
                                  SizedBox(
                                    height: 10.h,
                                  ),
                                  RadioButton(
                                      text: t.gender.female,
                                      isSelected:
                                          consumerValue.isSelectedList[0],
                                      value: Gender.Female,
                                      groupValue: consumerValue.currentGender,
                                      onChanged: (value) {
                                        consumerValue
                                            .changeCurrentGender(value);
                                        consumerValue
                                            .setTrueToIsSelectedList(0);
                                      }),
                                  SizedBox(
                                    height: 10.h,
                                  ),
                                  RadioButton(
                                      text: t.gender.male,
                                      isSelected:
                                          consumerValue.isSelectedList[1],
                                      value: Gender.Male,
                                      groupValue: consumerValue.currentGender,
                                      onChanged: (value) {
                                        consumerValue
                                            .changeCurrentGender(value);
                                        consumerValue
                                            .setTrueToIsSelectedList(1);
                                      }),
                                  SizedBox(
                                    height: 10.h,
                                  ),
                                  RadioButton(
                                      text: t.gender.other,
                                      isSelected:
                                          consumerValue.isSelectedList[2],
                                      value: Gender.Other,
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
                                const EdgeInsets.only(
                                    bottom: AppValues.kPadding * 2),
                            child: SizedBox(
                                height: 80,
                                child: GradientButton(
                                    onPressed: () {
                                      router.goNamed(AppViews.planView,
                                          extra: {"model": model});
                                    },
                                    isEnabled: consumerValue.isSelected,
                                    text: t.common.continue_action)),
                          ),
                        )
                      ]))))),
    );
  }
}
