import 'package:json_annotation/json_annotation.dart';

part 'action.g.dart';

@JsonSerializable()
class ActionModel {
  @JsonKey()
  final int id;

  @JsonKey()
  final String title;

  @JsonKey(name: 'image')
  final String imageUrl;

  ActionModel({
    required this.id,
    required this.title,
    required this.imageUrl,
  });

  factory ActionModel.fromJson(Map<String, dynamic> json) =>
      _$ActionModelFromJson(json);

  /// Connect the generated [_$ActionModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$ActionModelToJson(this);
}
