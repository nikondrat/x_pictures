import 'package:x_pictures/src/data.dart';

class StyleModel extends ItemModel {
  final String description;
  final List<String> data;
  final List<String>? images;

  final Function(ItemModel model)? onTap;
  final String? actionTitle;

  StyleModel(
      {required super.url,
      required super.title,
      required super.subTitle,
      required this.description,
      required this.data,
      this.images,
      this.onTap,
      this.actionTitle});
}
