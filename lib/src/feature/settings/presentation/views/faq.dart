import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class FaqView extends StatelessWidget {
  const FaqView({super.key});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        leading: const CustomBackButton(),
        title: Text(
          t.settings.help_center.faq,
          style: textTheme.bodyMedium!.copyWith(
            fontWeight: FontWeight.w700,
            fontSize: 17,
          ),
        ),
      ),
      body: AppBody(
          builder: (windowWidth, windowHeight, windowSize) => Padding(
              padding: HorizontalSpacing.centered(windowWidth),
              child: ListView(
                padding:
                    const EdgeInsets.symmetric(vertical: AppValues.kPadding),
                children: const [
                  // TODO change data
                  CustomExpansionTile(
                    title: 'hh',
                    content: 'Content',
                  ),
                ],
              ))),
    );
  }
}
