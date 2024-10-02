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
              child: ListView.builder(
                itemCount: t.settings.faq.titles.length,
                padding:
                    const EdgeInsets.symmetric(vertical: AppValues.kPadding),
                itemBuilder: (context, index) {
                  final String title = t.settings.faq.titles[index];
                  final String content = t.settings.faq.contents[index];

                  return CustomExpansionTile(title: title, content: content);
                },
              ))),
    );
  }
}
