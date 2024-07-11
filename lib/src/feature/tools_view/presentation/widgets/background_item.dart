import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class BackgroundItem extends StatelessWidget {
  final ItemModel model;
  final double? cardHeight;
  final Function(ItemModel model) onTap;
  const BackgroundItem(
      {super.key,
      required this.model,
      required this.cardHeight,
      required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
        width: 160,
        height: cardHeight ?? 240,
        margin: const EdgeInsets.only(right: AppValues.kPadding),
        child: ItemWithShadow(model: model, onTap: onTap));
  }
}
