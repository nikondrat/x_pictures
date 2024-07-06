import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class AllView extends StatelessWidget {
  final String title;
  final List<ItemModel> items;
  final Function(ItemModel model) onTap;
  const AllView(
      {super.key,
      required this.title,
      required this.onTap,
      required this.items});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
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
          children: items
              .map((e) => ItemWithShadow(model: e, onTap: (e) => onTap(e)))
              .toList(),
        ),
      ),
    );
  }
}
