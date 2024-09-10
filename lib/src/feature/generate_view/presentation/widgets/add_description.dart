import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
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

    final List<Tag> tags = [
      Tag(id: 0, title: 'Astronaut', categories: []),
      Tag(id: 0, title: 'Tropical staircase', categories: []),
      Tag(id: 0, title: 'Other', categories: []),
      Tag(id: 0, title: 'Other', categories: []),
      Tag(id: 0, title: 'Other', categories: []),
      Tag(id: 0, title: 'Other', categories: []),
      Tag(id: 0, title: 'Other', categories: []),
    ];

    return SafeArea(
      child: Padding(
        padding: EdgeInsets.only(bottom: mediaQueryData.viewInsets.bottom),
        child: SingleChildScrollView(
          padding: const EdgeInsets.only(bottom: AppValues.kPadding * 3),
          child: TitleWithBody(
              action: ResetButton(
                onPressed: () {
                  store.controller.clear();
                  for (var e in tags) {
                    e.setIsSelected(false);
                  }
                },
              ),
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
                              tags
                                  .map((e) => Observer(
                                      builder: (context) => ActionChip(
                                            onPressed: () {
                                              e.setIsSelected(!e.isSelected);
                                            },
                                            label: Text(e.title,
                                                style: textTheme.bodyLarge),
                                            backgroundColor: AppColors
                                                .kSecondaryAdditionallyColor,
                                            side: BorderSide(
                                                color: e.isSelected
                                                    ? AppColors.kPrimaryColor
                                                    : AppColors.kOutlineColor),
                                          )))
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
                      text: t.common.create),
                ],
              )),
        ),
      ),
    );
  }
}
