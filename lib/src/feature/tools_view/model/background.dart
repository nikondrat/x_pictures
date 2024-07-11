import 'package:x_pictures/src/data.dart';

class BackgroundSectionModel {
  final String title;

  final List<ItemModel> items;

  final double? cardHeight;

  BackgroundSectionModel({
    required this.title,
    required this.items,
    this.cardHeight,
  });
}
