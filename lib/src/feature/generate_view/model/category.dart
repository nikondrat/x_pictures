import 'package:json_annotation/json_annotation.dart';
import 'package:x_pictures/src/data.dart';

part 'category.g.dart';

@JsonSerializable()
class Category {
  @JsonKey()
  final int id;

  @JsonKey()
  final String title;

  @JsonKey(name: 'use_many_filters')
  final bool useManyFilters;

  @JsonKey()
  final List<Tag> filters;

  Category({
    required this.id,
    required this.title,
    required this.useManyFilters,
    required this.filters,
  });

  factory Category.fromJson(Map<String, dynamic> json) =>
      _$CategoryFromJson(json);

  /// Connect the generated [_$CategoryToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$CategoryToJson(this);
}
