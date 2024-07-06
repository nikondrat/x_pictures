import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/feature/template_view/presentation/widgets/cover_image_plan_page.dart';
import 'package:x_pictures/src/feature/template_view/state/plan.dart';
import 'package:x_pictures/src/core/constant/images.dart';

class PlanView extends StatelessWidget {
  const PlanView({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => PlanState(),
      child: Scaffold(
          floatingActionButton: Consumer<PlanState>(
              builder: (context, consumerValue, child) {
                return SizedBox(
                  height: 76.h,
                  child: Column(
                    children: [
                      Padding(
                        padding: EdgeInsets.only(left: 30.w),
                        child: SizedBox(
                          height: 50.h,
                          child: GradientButton(onPressed: () {
                            router.goNamed(AppViews.masterpieceView);
                          },
                            text: 'Continue',
                            isEnabled: consumerValue.isSelected,
                          ),
                        ),
                      ),
                      SizedBox(
                        height: 5.h,
                      ),
                      Padding(
                        padding: EdgeInsets.only(left: 30.w),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                              SizedBox(
                                height: 20.h,
                                child: TextButton(
                                    onPressed: () {},
                                    style: TextButton.styleFrom(
                                      padding: EdgeInsets.zero
                                    ),
                                    child: Text('Terms of Use',
                                      style: AppStyles.subTitleTextStyle.copyWith(
                                        fontSize: 10.sp,
                                      ),)),
                              ),
                            const Text(
                              '•',
                              style: TextStyle(color: Colors.white),
                            ),
                            SizedBox(
                              height: 20.h,
                              child: TextButton(
                                  onPressed: () {},
                                  style: TextButton.styleFrom(
                                      padding: EdgeInsets.zero
                                  ),
                                  child: Text('Privacy police',
                                    style: AppStyles.subTitleTextStyle.copyWith(
                                      fontSize: 10.sp,
                                    ),)),
                            ),
                            const Text(
                              '•',
                              style: TextStyle(color: Colors.white),
                            ),
                            SizedBox(
                              height: 20.h,
                              child: TextButton(
                                  onPressed: () {},
                                  style: TextButton.styleFrom(
                                      padding: EdgeInsets.zero
                                  ),
                                  child: Text('Restore Purchase',
                                    style: AppStyles.subTitleTextStyle.copyWith(
                                      fontSize: 10.sp,
                                    ),)),
                            ),
                          ],
                        ),
                      )
                    ],
                  ),
                );
              }
          ),
          body: Consumer<PlanState>(
            builder: (context, consumerValue, child) {
              return CustomScrollView(
                  slivers: <Widget> [
                    SliverToBoxAdapter(
                      child: CoverImagePlanPage(),
                    ),
                    SliverToBoxAdapter(
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
                        child: Column(
                          children: [
                            Text(
                              'Choose a plan',
                              style: AppStyles.head1TextStyle, textAlign: TextAlign.center,
                            ),
                            Text(
                              'This information will improve our selection of model images for the generation of your photos.',
                              style: AppStyles.subTitleTextStyle.copyWith(
                                fontSize: 17.sp,
                              ), textAlign: TextAlign.center,
                            ),
                            SizedBox(
                              height: 10.h,
                            ),
                            RadioButton(
                                text: '1 план',
                                isSelected: consumerValue.isSelectedList[0],
                                value: Plan.firstPlan,
                                groupValue: consumerValue.currentPlan,
                                onChanged: (value) {
                                  consumerValue.changeCurrentPlan(value);
                                  consumerValue.setTrueToIsSelectedList(0);
                                }),
                            SizedBox(
                              height: 10.h,
                            ),
                            RadioButton(
                                text: '2 план',
                                isSelected: consumerValue.isSelectedList[1],
                                value: Plan.secondPlan,
                                groupValue: consumerValue.currentPlan,
                                onChanged: (value) {
                                  consumerValue.changeCurrentPlan(value);
                                  consumerValue.setTrueToIsSelectedList(1);
                                }),
                            SizedBox(
                              height: 10.h,
                            ),
                            RadioButton(
                                text: '3 план',
                                isSelected: consumerValue.isSelectedList[2],
                                value: Plan.thirdPlan,
                                groupValue: consumerValue.currentPlan,
                                onChanged: (value) {
                                  consumerValue.changeCurrentPlan(value);
                                  consumerValue.setTrueToIsSelectedList(2);
                                }),
                          ],
                        ),
                      ),
                    )
                  ],
                  );
            }
          )
      ),
    );
  }
}
