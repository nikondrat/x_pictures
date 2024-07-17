import 'package:json_annotation/json_annotation.dart';

part 'filter.g.dart';

@JsonSerializable()
class FilterModel {
  @JsonKey(name: 'id')
  final int id;

  @JsonKey(name: 'title')
  final String title;

  FilterModel({
    required this.id,
    required this.title,
  });

  factory FilterModel.fromJson(Map<String, dynamic> json) =>
      _$FilterModelFromJson(json);

  /// Connect the generated [_$FilterModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$FilterModelToJson(this);
}
