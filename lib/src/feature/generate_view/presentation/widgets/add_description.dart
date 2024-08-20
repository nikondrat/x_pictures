import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:go_router/go_router.dart';
import 'package:x_pictures/src/data.dart';

class AddDescription extends StatelessWidget {
  final GenerateViewStore store;
  final GenerateStore genStore;
  const AddDescription(
      {super.key, required this.store, required this.genStore});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final MediaQueryData mediaQueryData = MediaQuery.of(context);

    return SafeArea(
      child: Padding(
        padding: EdgeInsets.only(bottom: mediaQueryData.viewInsets.bottom),
        child: SingleChildScrollView(
          child: TitleWithBody(
              action: const ResetButton(),
              title: t.generateView.add_description,
              child: Column(
                children: [
                  TextField(
                    maxLines: 5,
                    controller: store.controller,
                    decoration: InputDecoration(
                        filled: false,
                        hintText: t.generateView.input_hint,
                        contentPadding:
                            const EdgeInsets.all(AppValues.kPadding),
                        enabledBorder: OutlineInputBorder(
                            borderRadius:
                                BorderRadius.circular(AppValues.kRadius),
                            borderSide: const BorderSide(
                                color: AppColors.kOutlineColor)),
                        disabledBorder: OutlineInputBorder(
                            borderRadius:
                                BorderRadius.circular(AppValues.kRadius),
                            borderSide: const BorderSide(
                                color: AppColors.kOutlineColor)),
                        border: OutlineInputBorder(
                            borderRadius:
                                BorderRadius.circular(AppValues.kRadius),
                            borderSide: const BorderSide(
                                color: AppColors.kOutlineColor))),
                  ),
                  Gap(14.h),
                  ScrollConfiguration(
                    behavior:
                        ScrollConfiguration.of(context).copyWith(dragDevices: {
                      PointerDeviceKind.touch,
                      PointerDeviceKind.mouse,
                    }),
                    child: SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Wrap(
                          spacing: AppValues.kPadding,
                          children:
                              // TODO change this
                              [
                            'Astronaut',
                            'Tropical staircase',
                            'Other',
                            'Other',
                            'Other',
                            'Other',
                            'Other',
                            'Other'
                          ]
                                  .map((e) => ActionChip(
                                        onPressed: () {},
                                        label:
                                            Text(e, style: textTheme.bodyLarge),
                                        backgroundColor: AppColors
                                            .kSecondaryAdditionallyColor,
                                        side: const BorderSide(
                                            color: AppColors.kOutlineColor),
                                      ))
                                  .toList()),
                    ),
                  ),
                  Gap(14.h),
                  GradientButton(
                      onPressed: () {
                        context.pop();
                        genStore.generate();
                        // router.goNamed(AppViews.resultView);
                      },
                      text: t.common.create)
                ],
              )),
        ),
      ),
    );
  }
}
