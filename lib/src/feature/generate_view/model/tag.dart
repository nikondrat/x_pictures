import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'tag.g.dart';

@JsonSerializable()
class Tag {
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
