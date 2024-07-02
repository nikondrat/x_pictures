import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class GenerateView extends StatelessWidget {
  const GenerateView({super.key});

  @override
  Widget build(BuildContext context) {
    return Provider(
        create: (_) => GenerateViewStore(),
        child: Scaffold(
          appBar: AppBar(
            title: Text(t.generateView.title),
          ),
          body: AppBody(
            builder: (windowWidth, windowHeight, windowSize) {
              return SingleChildScrollView(
                  padding: HorizontalSpacing.centered(windowWidth),
                  child: Column(
                    children: [
                      const Gap(AppValues.kPadding),
                      const SelectModeWidget(),
                      const Gap(AppValues.kPadding),
                      const GenerateStyles(),
                      const Gap(AppValues.kPadding),
                      const GenerateTags(),
                      const Gap(AppValues.kPadding),
                      GenerateFormats(
                        windowHeight: windowHeight,
                      ),
                      const Gap(AppValues.kPadding),
                      const AddDescription(),
                      const Gap(AppValues.kPadding),
                    ],
                  ));
            },
          ),
        ));
  }
}
