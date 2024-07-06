import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/feature/template_view/enum/enum.dart';

class GenderView extends StatelessWidget {
  const GenderView({super.key});


  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => GenderState(),
      child: Scaffold(
          appBar: AppBar(
            leading: const CustomBackButton(),
            title: Text('Pick your gender'),
          ),
          floatingActionButton: Consumer<GenderState>(
            builder: (context, consumerValue, child) {
              return Padding(
                padding: EdgeInsets.only(left: 30.w),
                child: SizedBox(
                  height: 50.h,
                  child: GradientButton(onPressed: () {
                    router.goNamed(AppViews.planView);
                  },
                  text: 'Continue',
                    isEnabled: consumerValue.isSelected,
                  ),
                ),
              );
            }
          ),
          body: Consumer<GenderState>(
            builder: (context, consumerValue, child) {
              return Padding(
                padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
                child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Step 3 of 3',
                      style: AppStyles.subTitleTextStyle.copyWith(
                        fontSize: 10.sp,
                        ),),
                    SizedBox(
                      height: 5.h,
                        ),
                    Padding(
                      padding: EdgeInsets.only(right: 50.w),
                      child: Text(
                        'Pick your gender',
                        style: AppStyles.head1TextStyle,
                      ),
                    ),
                    SizedBox(
                      height: 5.h,
                    ),
                    Text(
                      'This information will improve our selection of model images for the generation of your photos.',
                      style: AppStyles.subTitleTextStyle.copyWith(
                        fontSize: 17.sp,
                      ),
                    ),
                    SizedBox(
                      height: 10.h,
                    ),
                    RadioButton(text: 'Female',
                        isSelected: consumerValue.isSelectedList[0],
                        value: Gender.Female,
                        groupValue: consumerValue.currentGender,
                        onChanged: (value) {
                          consumerValue.changeCurrentGender(value);
                          consumerValue.setTrueToIsSelectedList(0);
                        }),
                    SizedBox(
                      height: 10.h,
                    ),
                    RadioButton(text: 'Male',
                        isSelected: consumerValue.isSelectedList[1],
                        value: Gender.Male,
                        groupValue: consumerValue.currentGender,
                        onChanged: (value) {
                          consumerValue.changeCurrentGender(value);
                          consumerValue.setTrueToIsSelectedList(1);
                        }),
                    SizedBox(
                      height: 10.h,
                    ),
                    RadioButton(text: 'Other',
                        isSelected: consumerValue.isSelectedList[2],
                        value: Gender.Other,
                        groupValue: consumerValue.currentGender,
                        onChanged: (value) {
                          consumerValue.changeCurrentGender(value);
                          consumerValue.setTrueToIsSelectedList(2);
                        }),
                      ],
                    ),
              );
            }
          )
      ),
    );
  }
}
