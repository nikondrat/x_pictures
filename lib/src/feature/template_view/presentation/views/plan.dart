import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:x_pictures/src/core/constant/styles.dart';

class PlanView extends StatelessWidget {
  final PacksStore store;
  final LoraModel model;
  const PlanView({super.key, required this.store, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData theme = Theme.of(context);
    final TextTheme textTheme = theme.textTheme;

    return ChangeNotifierProvider(
      create: (context) => PlanState(),
      child: Scaffold(
          extendBodyBehindAppBar: true,
          appBar: AppBar(
            backgroundColor: Colors.transparent,
            leading: IconButton(
                onPressed: () => context.pop(), icon: const Icon(Icons.close)),
          ),
          body: DecoratedBox(
            decoration: BoxDecoration(
              image: DecorationImage(
                  image: Image.asset(Assets.images.pricesBanner.path).image,
                  fit: BoxFit.cover),
            ),
            child: Consumer<PlanState>(
                builder: (context, consumerValue, child) => Column(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: <Widget>[
                        Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: 15.w, vertical: 15.h),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              AutoSizeText(
                                t.plan.title,
                                style: textTheme.headlineSmall!.copyWith(
                                    fontSize: 24.sp,
                                    fontWeight: FontWeight.bold),
                                textAlign: TextAlign.center,
                              ),
                              Column(
                                children: t.template.additional_info.map((e) {
                                  return ListTile(
                                    dense: true,
                                    minLeadingWidth: 10.r,
                                    leading: CircleAvatar(
                                      radius: 4.r,
                                    ),
                                    title: AutoSizeText(
                                      e,
                                      style: textTheme.bodyLarge!
                                          .copyWith(fontSize: 17.sp),
                                    ),
                                  );
                                }).toList(),
                              ),
                              SizedBox(
                                height: 20.h,
                              ),
                              RadioButton(
                                  price: 7.99,
                                  text: t.plan.weekly,
                                  isSelected: consumerValue.isSelectedList[0],
                                  value: Plan.weekly,
                                  groupValue: consumerValue.currentPlan,
                                  onChanged: (value) {
                                    consumerValue.changeCurrentPlan(value);
                                    consumerValue.setTrueToIsSelectedList(0);
                                  }),
                              RadioButton(
                                  showDiscount: true,
                                  price: 0.87,
                                  subtitle: t.template.just(n: 44.99),
                                  text: t.plan.yearly,
                                  isSelected: consumerValue.isSelectedList[1],
                                  value: Plan.yearly,
                                  groupValue: consumerValue.currentPlan,
                                  onChanged: (value) {
                                    consumerValue.changeCurrentPlan(value);
                                    consumerValue.setTrueToIsSelectedList(1);
                                  }),
                              SizedBox(
                                height: 10.h,
                              ),
                            ],
                          ),
                        ),
                        Consumer<PlanState>(
                            builder: (context, consumerValue, child) {
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
                                          router.pushNamed(
                                              AppViews.masterpieceView,
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
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceEvenly,
                                      children: [
                                        SizedBox(
                                          height: 20.h,
                                          child: TextButton(
                                              onPressed: () {},
                                              style: TextButton.styleFrom(
                                                  padding: EdgeInsets.zero),
                                              child: AutoSizeText(
                                                t.common.terms_use,
                                                style: AppStyles
                                                    .subTitleTextStyle
                                                    .copyWith(
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
                                                style: AppStyles
                                                    .subTitleTextStyle
                                                    .copyWith(
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
                                                style: AppStyles
                                                    .subTitleTextStyle
                                                    .copyWith(
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
                        Gap(40.h)
                      ],
                    )),
          )),
    );
  }
}
