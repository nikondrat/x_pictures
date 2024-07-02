import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class AddDescription extends StatelessWidget {
  const AddDescription({super.key});

  @override
  Widget build(BuildContext context) {
    return TitleWithBody(
        action: const ResetButton(),
        title: t.generateView.add_description,
        child: Column(
          children: [
            TextField(
              maxLines: 5,
              decoration: InputDecoration(
                  filled: false,
                  hintText: t.generateView.input_hint,
                  contentPadding: const EdgeInsets.all(AppValues.kPadding),
                  border: const OutlineInputBorder()),
            ),
            const Gap(AppValues.kPadding),
            ScrollConfiguration(
              behavior: ScrollConfiguration.of(context).copyWith(dragDevices: {
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
                            .map((e) =>
                                ActionChip(onPressed: () {}, label: Text(e)))
                            .toList()),
              ),
            ),
            const Gap(AppValues.kPadding),
            GradientButton(
                onPressed: () {
                  router.goNamed(AppViews.resultView);
                },
                text: t.common.create)
          ],
        ));
  }
}
