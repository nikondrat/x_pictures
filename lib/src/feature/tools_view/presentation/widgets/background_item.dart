import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class BackgroundItem extends StatelessWidget {
  final PackModel model;
  final double? cardHeight;
  final Function(PackModel model) onTap;
  const BackgroundItem(
      {super.key, required this.model, this.cardHeight, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onDoubleTap: () {
        onTap(model);
      },
      child: Container(
          width: 160,
          height: cardHeight ?? 240,
          margin: const EdgeInsets.only(right: AppValues.kPadding),
          child: ItemWithShadow(model: model)),
    );
  }
}
