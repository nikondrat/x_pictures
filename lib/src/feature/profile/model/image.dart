import 'package:json_annotation/json_annotation.dart';

part 'image.g.dart';

@JsonSerializable()
class ImageModel {
  @JsonKey()
  final int id;

  @JsonKey(name: 'image')
  final String url;

  @JsonKey()
  final int? sort;

  @JsonKey(name: 'created')
  final DateTime? createdDate;

  ImageModel({
    required this.id,
    required this.url,
    this.sort,
    this.createdDate,
  });

  factory ImageModel.fromJson(Map<String, dynamic> json) =>
      _$ImageModelFromJson(json);

  /// Connect the generated [_$ImageModelToJson] function to the `toJson` method.
  Map<String, dynamic> toJson() => _$ImageModelToJson(this);
}
