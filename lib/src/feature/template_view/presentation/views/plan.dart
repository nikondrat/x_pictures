import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/feature/template_view/presentation/widgets/cover_image_plan_page.dart';

class PlanView extends StatelessWidget {
  final PacksStore store;
  final LoraModel model;
  const PlanView({super.key, required this.store, required this.model});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => PlanState(),
      child: Scaffold(
          body: Consumer<PlanState>(builder: (context, consumerValue, child) {
        return CustomScrollView(
          slivers: <Widget>[
            SliverToBoxAdapter(
              child: CoverImagePlanPage(),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
                child: Column(
                  children: [
                    AutoSizeText(
                      t.plan.title,
                      style: AppStyles.head1TextStyle.copyWith(fontSize: 17.sp),
                      textAlign: TextAlign.center,
                    ),
                    AutoSizeText(
                      t.plan.description,
                      style: AppStyles.subTitleTextStyle.copyWith(
                        fontSize: 12.sp,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    SizedBox(
                      height: 20.h,
                    ),
                    RadioButton(
                        text: t.plan.plan_first,
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
                        text: t.plan.plan_second,
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
                        text: t.plan.plan_third,
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
            ),
            SliverToBoxAdapter(
              child:
                  Consumer<PlanState>(builder: (context, consumerValue, child) {
                return Padding(
                    padding: EdgeInsets.symmetric(horizontal: 15.w),
                    child: SizedBox(
                      height: 100.h,
                      child: Column(
                        children: [
                          SizedBox(
                            // height: 50.h,
                            child: GradientButton(
                              onPressed: () {
                                router.pushNamed(AppViews.masterpieceView,
                                    extra: {
                                      'store': store,
                                      'model': model,
                                    });
                              },
                              text: t.common.continue_action,
                              isEnabled: consumerValue.isSelected,
                            ),
                          ),
                          SizedBox(
                            height: 5.h,
                          ),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                            children: [
                              SizedBox(
                                height: 20.h,
                                child: TextButton(
                                    onPressed: () {},
                                    style: TextButton.styleFrom(
                                        padding: EdgeInsets.zero),
                                    child: AutoSizeText(
                                      t.common.terms_use,
                                      style:
                                          AppStyles.subTitleTextStyle.copyWith(
                                        fontSize: 8.sp,
                                      ),
                                    )),
                              ),
                              AutoSizeText(
                                t.common.point,
                                style: TextStyle(color: Colors.white),
                              ),
                              SizedBox(
                                height: 20.h,
                                child: TextButton(
                                    onPressed: () {},
                                    style: TextButton.styleFrom(
                                        padding: EdgeInsets.zero),
                                    child: AutoSizeText(
                                      t.common.privacy_police,
                                      style:
                                          AppStyles.subTitleTextStyle.copyWith(
                                        fontSize: 8.sp,
                                      ),
                                    )),
                              ),
                              AutoSizeText(
                                t.common.point,
                                style: TextStyle(color: Colors.white),
                              ),
                              SizedBox(
                                height: 20.h,
                                child: TextButton(
                                    onPressed: () {},
                                    style: TextButton.styleFrom(
                                        padding: EdgeInsets.zero),
                                    child: AutoSizeText(
                                      t.common.restore_purchase,
                                      style:
                                          AppStyles.subTitleTextStyle.copyWith(
                                        fontSize: 8.sp,
                                      ),
                                    )),
                              ),
                            ],
                          )
                        ],
                      ),
                    ));
              }),
            ),
            SliverToBoxAdapter(
              child: Gap(40.h),
            )
          ],
        );
      })),
    );
  }
}
