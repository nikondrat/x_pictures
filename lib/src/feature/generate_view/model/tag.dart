// import 'package:json_annotation/json_annotation.dart';
// import 'package:x_pictures/src/data.dart';

// part 'tag.g.dart';

// @JsonSerializable()
// class Tag {
//   @JsonKey()
//   final int id;

//   @JsonKey()
//   final String title;

//   @JsonKey()
//   final List<Category> categories;

//   Tag({
//     required this.id,
//     required this.title,
//     required this.categories,
//   });

//   factory Tag.fromJson(Map<String, dynamic> json) => _$TagFromJson(json);

//   /// Connect the generated [_$TagToJson] function to the `toJson` method.
//   Map<String, dynamic> toJson() => _$TagToJson(this);
// }

import 'package:json_annotation/json_annotation.dart';
import 'package:mobx/mobx.dart';
import 'package:x_pictures/src/data.dart';

part 'tag.g.dart';

@JsonSerializable()
class Tag extends _Tag with _$Tag {
  @JsonKey()
  final int id;

  @JsonKey()
  final String title;

  @JsonKey()
  final List<Category> categories;

  Tag({
    required this.id,
    required this.title,
    required this.categories,
  });

  factory Tag.fromJson(Map<String, dynamic> json) => _$TagFromJson(json);

  /// Connect the generated [_$TagToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$TagToJson(this);
}

abstract class _Tag with Store {
  @observable
  @JsonKey(includeFromJson: false, includeToJson: false)
  bool isSelected = false;

  @action
  void setIsSelected(bool value) => isSelected = value;
}
