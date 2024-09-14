import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class AllView extends StatelessWidget {
  final String title;
  final List<PackModel> packs;
  final Function(PackModel model) onTap;
  const AllView(
      {super.key,
      required this.title,
      required this.onTap,
      required this.packs});

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          title,
          style: textTheme.bodyMedium!.copyWith(
            fontSize: 17,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
      body: AppBody(
        builder: (windowWidth, windowHeight, size) => GridView(
          padding: HorizontalSpacing.centered(windowWidth) +
              const EdgeInsets.only(top: AppValues.kPadding),
          gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
              maxCrossAxisExtent: 240,
              childAspectRatio: .7,
              mainAxisSpacing: AppValues.kPadding,
              crossAxisSpacing: AppValues.kPadding),
          children: packs
              .map((e) => GestureDetector(
                  onTap: () {
                    onTap(e);
                  },
                  child: ItemWithShadow(model: e)))
              .toList(),
        ),
      ),
    );
  }
}
